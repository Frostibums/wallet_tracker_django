import cloudscraper
import requests

from wallet_tracker.settings import SCANNERS_API_KEYS
from wallets.models import Wallet, Blockchain


def get_new_txs(wallet: Wallet,
                blockchain: Blockchain,
                offset: int = 5,
                start_block: int = 0) -> list:
    """Retrieve new transactions for a wallet using a blockchain scanner API.

    Args:
        wallet (Wallet): The wallet for which transactions are to be retrieved.
        blockchain (Blockchain): The blockchain name (e.g., 'bsc', 'eth', 'op').
        offset (int): The number of transactions to retrieve (default is 5).
        start_block (int): The starting block to search from (default is 0).

    Returns:
        list: A list of new transactions.
    """
    data = {
        'module': 'account',
        'action': '',
        'address': wallet.wallet_address,
        'apikey': SCANNERS_API_KEYS.get(blockchain.title),
        'offset': offset,
        'startblock': start_block,
        'sort': 'desc',
        'page': 1,
    }
    scanner_api = {
        'bsc': 'https://api.bscscan.com/api',
        'eth': 'https://api.etherscan.io/api',
        'op': 'https://api-optimistic.etherscan.io/api',
    }
    new_txs = []
    # Using a switch-case like structure for different blockchain actions (To add solana or atom in future)
    match str(blockchain.title):
        case 'bsc' | 'eth' | 'op':
            actions = ['tokentx', 'txlist']
            for action in actions:
                data['action'] = action
                txs = requests.get(scanner_api.get(blockchain.title), params=data).json()
                if txs.get('message') == 'OK':
                    new_txs.extend(txs.get('result'))

        case _:
            raise ValueError(f'{blockchain.title} is not an option yet.')
    return new_txs


def get_bsc_bnb_value(wallet_address: str) -> float | bool:
    """Receive the Binance BNB balance of a wallet using a blockchain scanner API.

    Args:
        wallet_address (str): The wallet address.

    Returns:
        float|bool: The BNB balance if available, else False.
    """
    data = {
        'module': 'account',
        'action': 'balance',
        'address': wallet_address,
        'apikey': SCANNERS_API_KEYS.get('bsc'),
    }
    value_request = requests.get('https://api.bscscan.com/api', params=data).json()
    if value_request.get('message') == 'OK':
        value = value_request.get('result')
        return value
    return False


def check_if_bsc_wallet_exists(wallet_address: str) -> bool:
    """Check if a Binance Smart Chain (BSC) wallet exists.

    Args:
        wallet_address (str): The BSC wallet address.

    Returns:
        bool: True if the wallet exists, False otherwise.
    """
    link = f'https://bscscan.com/address/{wallet_address}'
    if 'Binance Account (Invalid Address)' in get_page(link):
        return False
    return True


def get_page(link: str) -> str:
    """Retrieve the content of a web page using a cloudscraper to bypass cloudflare.

    Args:
        link (str): The URL of the web page.

    Returns:
        str: The HTML content of the web page.
    """
    scraper = cloudscraper.CloudScraper()
    return scraper.get(link).text
