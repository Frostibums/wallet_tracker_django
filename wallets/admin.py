from django.contrib import admin

from wallets.models import Wallet, Blockchain, Transaction

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Blockchain)
admin.site.register(Transaction)