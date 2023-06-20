from wallet_tracker.settings import SCANNERS_API_KEYS
import requests
import cloudscraper


def get_new_txs(wallet, blockchain, offset=5, start_block=0):
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
    match str(blockchain.title):
        case 'bsc' | 'eth' | 'op':
            actions = ['tokentx', 'txlist']
            for action in actions:
                data['action'] = action
                txs = requests.get(scanner_api.get(blockchain.title), params=data).json()
                if txs.get('message') == 'OK':
                    for tx in txs.get('result'):
                        new_txs.append(tx)
        case _:
            print(blockchain.title)
    return new_txs


def get_bsc_bnb_value(wallet_address):
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


def check_if_bsc_wallet_exists(wallet_address):
    link = f'https://bscscan.com/address/{wallet_address}'
    if 'Binance Account (Invalid Address)' in get_page(link):
        return False
    return True


def get_page(link):
    scraper = cloudscraper.CloudScraper()
    return scraper.get(link).text

