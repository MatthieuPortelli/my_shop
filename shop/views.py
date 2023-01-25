import random
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, Category, Cart, Order, Address


def index(request):
    # Je récupère toutes les Category de la BDD
    category_object = Category.objects.all()

    # Je récupère tous les Product de la BDD puis j'en sélectionne 6 au hasard pour les afficher sur ma home page
    items = list(Product.objects.all())
    product_object = random.sample(items, 6)

    # Je récupère la valeur de l'input de recherche
    item_name = request.GET.get('item-name')
    if item_name != '' and item_name is not None:
        # Je cherche dans les objets de la BDD s'il en existe un avec le nom indiqué dans l'input
        product_object = Product.objects.filter(name__icontains=item_name)

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    context = {
        'product_object': product_object,
        'category_object': category_object,
        'total_number_products': total_number_products,
    }

    return render(request, 'shop/index.html', context)


def products(request):
    # Je récupère tous les objets Product
    product_object = Product.objects.all()

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    # Pagination, on passe l'objet et le nombre d'objets que l'on veut afficher
    paginator = Paginator(product_object, 12)
    page_number = request.GET.get('page')
    product_object = paginator.get_page(page_number)

    context = {
        'product_object': product_object,
        'category_object': category_object,
        'total_number_products': total_number_products
    }

    return render(request, 'shop/products.html', context)


def product_detail(request, slug):
    # Je récupère l'objet s'il existe sinon erreur 404
    product_object = get_object_or_404(Product, slug=slug)

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    context = {
        'product': product_object,
        'category_object': category_object,
        'total_number_products': total_number_products
    }

    return render(request, 'shop/product_detail.html', context)


def categories(request):
    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    context = {
        'category_object': category_object,
        'total_number_products': total_number_products
    }

    return render(request, 'shop/categories.html', context)


def categories_products(request, slug):
    # Si une Category avec ce slug existe
    if Category.objects.filter(slug=slug):
        # Je récupère toutes les catégories
        category_object = Category.objects.all()

        # Je récupère les produits de cette Category
        products = Product.objects.filter(category__slug=slug)

        # Je récupère le nom de la Category
        category_name = Category.objects.filter(slug=slug).first()

        # Je récupère le nombre d'articles dans le panier
        total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

        context = {
            'products': products,
            'category_name': category_name,
            'category_object': category_object,
            'total_number_products': total_number_products,
        }

        return render(request, 'shop/category_detail.html', context)
    else:
        messages.error(request, "Cette catégorie n'existe pas.")
        return redirect('categories')


@login_required(login_url='login')
def add_to_cart(request, slug):
    # Je récupère l'utilisateur
    user = request.user
    # Je récupère le produit s'il existe
    product = get_object_or_404(Product, slug=slug)
    # objects = manager des objets, je veux récupérer le panier associé à l'utilisateur, s'il n'existe pas je le crée
    # La méthode get_or_create va retourner l'objet et l'information sur le fait que l'objet a été créé ou non
    # Cette info est stockée dans '_', c'est une convention pour signaler que je ne vais pas l'utiliser
    cart, _ = Cart.objects.get_or_create(user=user)
    # Je regarde si j'ai déjà le produit que je rajoute dans ma commande, je cible les articles qui n'ont pas déjà été commandés
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)

    # Si le produit n'était pas dans la commande, je le rajoute et je sauvegarde le panier
    if created:
        cart.orders.add(order)
        cart.save()
    # S'il était déjà dans la commande, j'en rajoute un et je sauvegarde la commande
    else:
        order.quantity += 1
        order.save()

    # Je diminue le stock
    product.stock -= 1
    product.save()

    # Redirection sur la page en cours
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def remove_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)

    if order.quantity > 1:
        order.quantity -= 1
    order.save()

    # J'augmente le stock
    product.stock += 1
    product.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def cart(request):
    # Je récupère le panier de l'utilisateur s'il existe (objet de type Cart, l'utilisateur associé à la requête)
    try:
        cart = get_object_or_404(Cart, user=request.user)
    except:
        # Je récupère toutes les catégories
        category_object = Category.objects.all()

        return render(request, 'shop/cart.html', context={'category_object': category_object})

    # Je récupère le nombre d'articles dans le panier
    # The aggregate() method returns a dictionary. If you know you're only returning a single-entry dictionary you could use .values()[0]
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    # GET: il n'attend qu'un seul élément, le Order en cours lié à l'utilisateur
    # order_get = cart.orders.get(user=request.user)
    # Je ne peux donc avoir que le total de ce seul Order
    # total_price = order_get.product.price * order_get.quantity
    # FILTER: pour 2 ou plus
    order_filter = list(cart.orders.filter(user=request.user).aggregate(total=Sum(F('quantity') * F('product__price'))).values())[0]

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'orders': cart.orders.all(),
        'category_object': category_object,
        'total_price': order_filter,
        'total_number_products': total_number_products,
    }

    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def validate_cart(request):
    # Je récupère le panier de l'utilisateur s'il existe (objet de type Cart, l'utilisateur associé à la requête)
    try:
        cart = get_object_or_404(Cart, user=request.user)
    except:
        # Je récupère toutes les catégories
        category_object = Category.objects.all()

        return render(request, 'shop/cart.html', context={'category_object': category_object})

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    # Je recupère le montant de la commande
    total_price = list(cart.orders.filter(user=request.user).aggregate(total=Sum(F('quantity') * F('product__price'))).values())[0]

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'total_price': total_price,
        'total_number_products': total_number_products,
        'category_object': category_object,
    }

    return render(request, 'shop/address.html', context)


@login_required(login_url='login')
def delete_cart(request):
    if cart := request.user.cart:
        # Tous les Order dans Cart
        orders = cart.orders.all().values()
        # Pour remettre à jour les stocks, pour cahque Order dans le Cart
        for order in orders:
            # Je récupère la quantité commandé dans l'Order
            order_quantity = order['quantity']
            # Je récupère le Product commandé dans l'Order grâce à l'id récupérée dans le dictionnaire
            product_order = Product.objects.get(id=order['product_id'])
            # J'augmente la stock du Product de la quantité commandée dans l'Order
            product_order.stock += order_quantity
            product_order.save()

        # Je nettoie tous les produits (orders)
        cart.orders.all().delete()
        # Appel à la fonction true_delete() de models.py
        cart.true_delete()

        messages.info(request, "Le panier a été supprimé.")

    return redirect('/')


@login_required(login_url='login')
def address_cart(request):
    # Je récupère le panier de l'utilisateur s'il existe (objet de type Cart, l'utilisateur associé à la requête)
    try:
        cart = get_object_or_404(Cart, user=request.user)
    except:
        # Je récupère toutes les catégories
        category_object = Category.objects.all()

        return render(request, 'shop/cart.html', context={'category_object': category_object})

    # Je récupère le nombre d'articles dans le panier
    total_number_products = list(Order.objects.filter(ordered=False).aggregate(Sum('quantity')).values())[0]

    # Je recupère le montant de la commande
    total_price = list(cart.orders.filter(user=request.user).aggregate(total=Sum(F('quantity') * F('product__price'))).values())[0]

    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'total_price': total_price,
        'total_number_products': total_number_products,
        'category_object': category_object,
    }

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        street = request.POST.get('street')
        postalcode = request.POST.get('postalcode')
        city = request.POST.get('city')

        address = Address(firstname=firstname,
                          lastname=lastname,
                          street=street,
                          postalcode=postalcode,
                          city=city)
        # Je sauvegarde pour générer l'id auto
        address.save()

        # Opérateur walrus := (tête de morse), méthode plus concise (vérification 'Si le panier existe' et assignation en une ligne)
        if cart := request.user.cart:
            # Appel à la fonction surchargée delete() de models.py
            cart.delete()

        return redirect('confirm-cart')

    return render(request, 'shop/address.html', context)


@login_required(login_url='login')
def confirm_cart(request):
    # Je veux récupérer le prénom dans l'adresse nouvellement créée
    info = Address.objects.all()[:1]

    # TODO: vérifier le prénom envoyé
    for item in info:
        firstname = item.firstname

    return render(request, 'shop/confirm.html', {'firstname': firstname})


def legal(request):
    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'category_object': category_object,
    }

    return render(request, 'shop/legal.html', context)


def conditions(request):
    # Je récupère toutes les catégories
    category_object = Category.objects.all()

    context = {
        'category_object': category_object,
    }

    return render(request, 'shop/conditions.html', context)
