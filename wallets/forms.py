from django import forms
from django.core.exceptions import ValidationError

from .models import Wallet
from .services import get_wallet
from .parser import check_if_bsc_wallet_exists


class WalletAddForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['wallet_address', 'blockchains']
        widgets = {
            'blockchains': forms.CheckboxSelectMultiple,
        }

    def has_no_duplicates(self):
        if get_wallet(self.cleaned_data.get('wallet_address')):
            return False
        return True

    def exists(self):
        return check_if_bsc_wallet_exists(self.cleaned_data.get('wallet_address'))

    def validate(self):
        if not self.exists():
            self.add_error('wallet_address', ValidationError('Wallet with such address doesn\'t exist.'))

        if not self.has_no_duplicates():
            self.add_error('wallet_address', ValidationError('Wallet with such address is already added.'))

        return self.cleaned_data.get('wallet_address')
