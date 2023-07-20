from datetime import datetime

from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404

from wallets.models import Transaction, Wallet


def get_all_wallets_addresses():
    return list(Wallet.objects.all().values_list('wallet_address', flat=True))


def get_wallet_blockchains(wallet):
    return wallet.blockchains.all()


def get_wallet(wallet_address):
    try:
        wallet = get_object_or_404(Wallet, wallet_address=wallet_address)
        return wallet
    except Http404:
        return False


def get_user_wallets(user):
    try:
        wallets = get_list_or_404(Wallet, owner=user)
        return wallets
    except Http404:
        return []


def remove_wallet_from_user(wallet_address):
    wallet = get_wallet(wallet_address)
    if wallet:
        wallet.delete()


def get_wallet_owner(wallet_address):
    wallet = get_wallet(wallet_address)
    if not wallet:
        return ''
    return wallet.owner


def get_last_block(wallet, blockchain):
    try:
        return Transaction.objects.filter(wallet=wallet, blockchain=blockchain).aggregate(Max('block_number'))
    except Http404:
        return 0


def add_tx_to_wallet(wallet, tx, blockchain):
    new_tx, created = Transaction.objects.get_or_create(
        wallet=wallet,
        blockchain=blockchain,
        block_number=tx.get('blockNumber'),
        hash=tx.get('hash'),
        tx_from=tx.get('from'),
        tx_to=tx.get('to'),
        token_name=tx.get('tokenName', ''),
        token_symbol=tx.get('tokenSymbol', blockchain),
        value=str(round(int(tx.get('value')) / 10 ** 18, 2)),
        time_stamp=datetime.fromtimestamp(int(tx.get('timeStamp'))),
    )
    return created


def get_wallet_txs(wallet, amount=5):
    txs = {}
    for blockchain in get_wallet_blockchains(wallet):
        txs[blockchain] = Transaction.objects.filter(wallet=wallet, blockchain=blockchain).order_by('-time_stamp')[:amount]
    return {
        'wallet': wallet,
        'txs': txs,
    }
