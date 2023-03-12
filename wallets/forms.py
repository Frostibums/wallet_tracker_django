from django import forms
from django.core.exceptions import ValidationError

from .models import Wallet
from .parser import check_if_bsc_wallet_exists


class WalletAddForm(forms.ModelForm):
    def has_no_duplicates(self):
        return True

    def exists(self):
        if check_if_bsc_wallet_exists(self.cleaned_data.get('wallet_address')):
            return True
        self.add_error('wallet_address', ValidationError('Wallet with such address doesn\'t exist.'))


    class Meta:
        model = Wallet
        fields = ['wallet_address', 'blockchains']
        widgets = {
            'blockchains': forms.CheckboxSelectMultiple,
        }