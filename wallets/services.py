from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Max, QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404

from wallets.models import Blockchain, Transaction, Wallet


def get_all_wallets_addresses() -> list[Wallet]:
    """Get a list of all wallet addresses in the database."""
    return list(Wallet.objects.all().values_list('wallet_address', flat=True))


def get_wallet_blockchains(wallet: Wallet) -> QuerySet[Blockchain]:
    """Get the blockchains associated with a wallet."""
    return wallet.blockchains.all()


def get_wallet(wallet_address: str) -> Wallet | bool:
    """Get a wallet (Wallet) by its wallet address or False if not found."""
    try:
        wallet = get_object_or_404(Wallet, wallet_address=wallet_address)
        return wallet
    except Http404:
        return False


def get_user_wallets(user: User) -> QuerySet[Wallet]:
    """Get wallets associated with a user."""
    wallets = Wallet.objects.filter(owner=user)
    return wallets


def remove_wallet_from_user(wallet_address: str) -> None:
    """Remove a wallet from a user's account."""
    wallet = get_wallet(wallet_address)
    if wallet:
        wallet.delete()


def get_wallet_owner(wallet_address: str) -> User | str:
    """Get the owner (User) of a wallet or '' if not found."""
    wallet = get_wallet(wallet_address)
    if not wallet:
        return ''
    return wallet.owner


def get_last_block(wallet: Wallet, blockchain: Blockchain) -> Transaction | None:
    """Get the last block number for a last wallet transaction in the database for specific blockchain."""
    last_block = Transaction.objects.filter(wallet=wallet, blockchain=blockchain).aggregate(Max('block_number'))
    last_block_number = last_block.get('block_number__max')
    return last_block_number if last_block_number is not None else 0


def add_tx_to_wallet(wallet: Wallet, tx: dict, blockchain: Blockchain):
    """Add a transaction to a wallet's transaction history.

    Args:
        wallet (Wallet): The wallet to which the transaction belongs.
        tx (dict): The transaction data.
        blockchain (Blockchain): The blockchain for which to add the transaction.

    Returns:
        bool: True if the transaction was created, False if it already exists.
    """
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


def get_wallet_txs(wallet: Wallet, amount: int = 5):
    """Get a wallet's transactions.

    Args:
        wallet (Wallet): The wallet for which to retrieve transactions.
        amount (int): The number of last transactions to retrieve (default is 5).

    Returns:
        dict: A dictionary containing wallet and transactions information.
    """
    txs = {}
    for blockchain in get_wallet_blockchains(wallet):
        txs[blockchain] = Transaction.objects.filter(wallet=wallet, blockchain=blockchain).order_by('-time_stamp')[
                          :amount]
    return {
        'wallet': wallet,
        'txs': txs,
    }
