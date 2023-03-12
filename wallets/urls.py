from django.urls import path

from . import views

urlpatterns = [
    path('', views.wallets_list, name='wallets_list'),
    path('add/', views.add_wallet, name='wallet_add'),
    path('remove/<str:wallet_address>', views.remove_wallet, name='wallet_remove'),
]
