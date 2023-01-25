from django.contrib import admin
from django.contrib.auth.models import User

from shop.models import Category, Product, Order, Cart, Address


# Pour modifier l'affichage dans la section admin
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'date_added')


class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'id', 'slug', 'price', 'stock', 'get_product_category', 'date_added')

    @admin.display(description='Category')
    def get_product_category(self, obj):
        return obj.category.name


class AdminOrder(admin.ModelAdmin):
    model = Product, User
    list_display = ('get_product_name', 'id', 'quantity', 'get_user_name', 'ordered', 'ordered_date')

    @admin.display(description='Product')
    def get_product_name(self, obj):
        return obj.product.name

    @admin.display(description='User')
    def get_user_name(self, obj):
        return obj.user.username


class AdminCart(admin.ModelAdmin):
    list_display = ('get_user_name', 'id')

    @admin.display(description='User')
    def get_user_name(self, obj):
        return obj.user.username


class AdminAddress(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'street', 'postalcode', 'city')


admin.site.register(Category, AdminCategory)
admin.site.register(Product, AdminProduct)
admin.site.register(Order, AdminOrder)
admin.site.register(Cart, AdminCart)
admin.site.register(Address, AdminAddress)
