from django.contrib.auth.models import User

from rest_framework import serializers

from wallets.models import Wallet
from wallets.parser import check_if_bsc_wallet_exists
from wallets.services import get_wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    blockchains = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = Wallet
        exclude = ('owner', )


class WalletAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['wallet_address', 'blockchains']

    def _is_duplicate(self):
        return get_wallet(self.data.get('wallet_address')) is not False

    def _exists(self):
        return check_if_bsc_wallet_exists(self.data.get('wallet_address'))

    def validate_wallet(self):
        if not self._exists():
            raise serializers.ValidationError('Wallet with such address doesn\'t exist.')

        if self._is_duplicate():
            raise serializers.ValidationError('Wallet with such address is already added.')

        return self.data.get('wallet_address')