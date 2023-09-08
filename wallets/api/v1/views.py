from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wallets.models import Wallet

from .serializers import WalletAddSerializer, WalletSerializer
from ...services import get_wallet_owner
from ...tasks import update_wallet_txs


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_wallets(request):
    """Retrieve a list of wallets owned by the authenticated user."""
    user = request.user
    wallets = Wallet.objects.filter(owner=user)
    serializer = WalletSerializer(wallets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_wallet(request):
    """Add a new wallet for the authenticated user."""
    data = request.data
    wallet_address = data.get('wallet_address')
    blockchains = data.get('blockchains')

    if not all([wallet_address, blockchains]):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = WalletAddSerializer(data={'wallet_address': wallet_address, 'blockchains': blockchains})

    if not all([serializer.is_valid(), serializer.validate_wallet()]):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    new_wallet = Wallet.objects.create(
        wallet_address=validated_data['wallet_address'],
        owner=request.user,
    )
    new_wallet.save()
    new_wallet.blockchains.add(*blockchains)
    update_wallet_txs.delay(new_wallet.wallet_address)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_wallet(request, wallet_address):
    """Remove a wallet owned by the authenticated user."""
    if request.user != get_wallet_owner(wallet_address):
        return Response(status=status.HTTP_403_FORBIDDEN)
    wallet = Wallet.objects.filter(wallet_address=wallet_address)
    wallet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
