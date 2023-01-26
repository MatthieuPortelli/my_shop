from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from shop.models import Order, Category
from .forms import SignUpForm
from .token import account_activation_token
import re


def activate(request, uidb64, token):
    User = get_user_model()
    # J'essaie de décoder le lien reçu
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    # Si l'utilisateur existe et que le token a été vérifié, je passe celui-ci en actif, j'enregistre et je redirige
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f"Merci pour la confirmation de votre compte, vous pouvez maintenant vous connecter.")
        return redirect('login')
    else:
        messages.error(request, "Le lien d'activation est invalide.")

    return redirect('/')


def activateEmail(request, user, to_email):
    # Création de l'email d'activation du compte
    mail_subject = "Activation de votre compte utilisateur"
    message = render_to_string("account/emailconfirm.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.info(request, f"Bonjour {user}, allez sur votre email {to_email} et cliquez sur le lien pour confirmer votre inscription.")
    else:
        messages.error(request, f"Une erreur est survenue lors de l'envoi de l'email, veuillez vérifier l'adresse indiquée.")


def signup(request):
    # Si l'utilisateur est connecté, je ne veux pas qu'il accède à la view signup
    if request.user.is_authenticated:
        return redirect('/')

    # Au submit du form
    if request.method == "POST":
        # Je récupère les valeurs des inputs
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Controle username
        if username == '' or username is None:
            messages.error(request, "Veuillez indiquer un nom d'utilisateur.")
            return redirect('signup')
        if len(username) < 3:
            messages.error(request, "Le nom d'utilisateur doit comporter au minimum 3 caractères.")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('signup')

        # Controle email
        if email == '' or email is None:
            messages.error(request, "Veuillez indiquer un email.")
            return redirect('signup')
        if not validate_email_address(email):
            messages.error(request, "L'e-mail n'est pas valide.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet e-mail est déjà pris.")
            return redirect('signup')

        # Controle password
        if password1 == '' or password1 is None:
            messages.error(request, "Veuillez indiquer un mot de passe.")
            return redirect('signup')
        if not validate_password(password1):
            messages.error(request, "Le mot de passe doit contenir au minimum 8 caractères, au moins une majuscule, une minuscule, un chiffre et un caractère spécial.")
            return redirect('signup')
        if password1 != password2:
            messages.error(request, "Les mots de passe sont différents.")
            return redirect('signup')

        form = SignUpForm(request.POST)

        if form.is_valid():
            # Création de l'utilisateur
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password1)

            # Je veux pouvoir activer le compte via un mail
            # --- Désactivé le temps de gérer le captcha ---
            # user.is_active = False
            user.is_active = True
            # Je sauvegarde
            user.save()

            # Fonction d'activation du compte par email
            # --- Désactivé le temps de gérer le captcha ---
            # activateEmail(request, user, email)

            # Connection de l'utilisateur
            login(request, user)

            return redirect('/')
        else:
            print('INVALID')
            messages.error(request, "Veuillez cocher la case reCAPTCHA.")
    else:
        form = SignUpForm()

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'category_object': category_object,
        'form': form,
    }

    return render(request, 'account/signup.html', context)


def custom_login(request):
    # Si l'utilisateur est connecté, je ne veux pas qu'il accède à la view signin
    if request.user.is_authenticated:
        return redirect('/')

    # Je test la validité du formulaire
    if request.method == 'POST':
        # Je récupère les informations des inputs
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # Contrôle du username
        if username == "":
            messages.error(request, "Veuillez indiquer un nom d'utilisateur.")
            return redirect('login')

        # Contrôle du password
        if password == "":
            messages.error(request, "Veuillez indiquer un mot de passe.")
            return redirect('login')

        # Si l'utilisateur existe en BDD, je le connecte et je redirige sur la view index
        if user is not None:
            login(request, user)
            messages.info(request, "Vous êtes connecté.")
            return redirect('/')
        # Sinon je lui indique un message d'erreur et je le redirige sur le formulaire
        else:
            messages.error(request, 'Informations de connexion incorrectes.')
            return redirect('login')

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'category_object': category_object,
    }

    return render(request, 'account/login.html', context)


@login_required(login_url='login')
def custom_logout(request):
    # Je déconnecte
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")

    # Je retourne sur l'index
    return redirect('/')


def validate_email_address(email_address):
    # Validation email REGEX
    return re.search(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email_address)


def validate_password(password):
    # Validation email REGEX
    return re.search(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}', password)


@login_required(login_url='login')
def account(request):
    # Je récupère l'utilisateur courant
    current_user = request.user

    # Je récupère les commandes de l'utilisateur
    orders = Order.objects.filter(user=request.user)

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    context = {
        'user': current_user,
        'orders': orders,
        'category_object': category_object,
        'total_number_products': total_number_products
    }

    return render(request, 'account/account.html', context)
