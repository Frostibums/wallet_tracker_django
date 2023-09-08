from django.urls import path

from wallets.api.v1 import views

urlpatterns = [
    path('get_wallets/', views.get_user_wallets, name='api_get_wallets'),
    path('add_wallet/', views.add_wallet, name='api_add_wallet'),
    path('remove_wallet/<str:wallet_address>/', views.remove_wallet, name='api_remove_wallet'),
]
