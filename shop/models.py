from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=2000, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True)

    # Pour modifier l'ordre par défaut des objets, je souhaite alphabétique
    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.CharField(max_length=2000, blank=True)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    # Pour avoir accès à un lien dans la section admin pour la page du produit sur le site
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(blank=True, null=True)

    # Pour la section admin
    def __str__(self):
        return f"{self.product.name} ({self.quantity}) {self.user.username} {self.ordered} {self.ordered_date}"

    # def get_products(self):
    #     products = Order.product.all()
    #     return products


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    # Pour la section admin
    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        # Surcharge de la méthode delete, je veux aussi supprimer tous les articles de la commande lorsque je suis dans la section admin ou en ligne de commande
        # Je boucle sur tous les articles attachés au panier
        for order in self.orders.all():
            order.ordered = True
            # Je date la commande de l'article, par défaut en UTC
            order.ordered_date = timezone.now()
            order.save()

        # Je vide le panier, j'enlève les éléments
        self.orders.clear()
        super().delete(*args, **kwargs)

    def true_delete(self, *args, **kwargs):
        # Je vide le panier, j'enlève les éléments
        self.orders.clear()
        super().delete(*args, **kwargs)


class Address(models.Model):
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200, blank=True, null=True)
    postalcode = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)

    # Pour la section admin
    def __str__(self):
        return f"{self.firstname} ({self.lastname})"
