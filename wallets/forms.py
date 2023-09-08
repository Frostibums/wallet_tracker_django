from django import forms
from django.core.exceptions import ValidationError

from .models import Wallet
from .parser import check_if_bsc_wallet_exists
from .services import get_wallet


class WalletAddForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['wallet_address', 'blockchains']
        widgets = {
            'blockchains': forms.CheckboxSelectMultiple,
        }

    def _is_duplicate(self):
        return get_wallet(self.cleaned_data.get('wallet_address')) is not False

    def _exists(self):
        return check_if_bsc_wallet_exists(self.cleaned_data.get('wallet_address'))

    def validate(self):
        if not self._exists():
            self.add_error('wallet_address', ValidationError('Wallet with such address doesn\'t exist.'))

        if self._is_duplicate():
            self.add_error('wallet_address', ValidationError('Wallet with such address is already added.'))

        return self.cleaned_data.get('wallet_address')
