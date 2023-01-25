from django.urls import path
from shop.views import index, product_detail, products, categories, categories_products, add_to_cart, cart, delete_cart, \
    validate_cart, remove_to_cart, address_cart, confirm_cart, legal, conditions

urlpatterns = [
    path('', index, name='home'),
    path('product/<str:slug>/', product_detail, name="product"),
    path('products/', products, name="products"),
    path('categories/', categories, name="categories"),
    path('categories/<str:slug>/', categories_products, name="categories-products"),
    path('add-to-cart/<str:slug>/', add_to_cart, name="add-to-cart"),
    path('remove-to-cart/<str:slug>/', remove_to_cart, name="remove-to-cart"),
    path('cart/', cart, name="cart"),
    path('cart/validate', validate_cart, name='validate-cart'),
    path('cart/delete', delete_cart, name='delete-cart'),
    path('cart/address', address_cart, name='address-cart'),
    path('cart/confirm', confirm_cart, name='confirm-cart'),
    path('legal/', legal, name='legal'),
    path('conditions/', conditions, name='conditions'),
]
