from django.urls import path
from account.views import signup, custom_login, custom_logout, activate, account

urlpatterns = [
    path('signup/', signup, name="signup"),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('account/', account, name='account'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]
