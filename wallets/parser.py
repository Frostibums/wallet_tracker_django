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



# def get_bsc_txs(wallet, offset=5, start_block=0):
#     data = {
#         'module': 'account',
#         'action': 'tokentx',
#         'address': wallet.wallet_address,
#         'apikey': BSCSCAN_API_KEY,
#         'offset': offset,
#         'startblock': start_block,
#         'sort': 'desc',
#         'page': 1,
#     }
#     txs_request = requests.get('https://api.bscscan.com/api', params=data).json()
#     if txs_request.get('message') == 'OK':
#         txs = txs_request.get('result')
#         return txs


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

#print(check_if_bsc_wallet_exists('0xe93524efb635d9708072f763d741d1b84c0c4'))
#print(check_if_bsc_wallet_exists('0x07B49A36b33621edFbA7ccDCE6b96997ea1Ef2e3'))

# import cloudscraper
# from bs4 import BeautifulSoup
# import re

# def get_blockchain_wallet_link(wallet):
#     address_map = {
#         'bsc': 'https://bscscan.com/address/',
#
#     }
#     return f'{address_map.get(wallet.blockchain)}{wallet.wallet_address}'
#
#
# def get_page(link):
#     scraper = cloudscraper.CloudScraper()
#     return scraper.get(link).text
#
#
# def get_tx_data(tx):
#     tx_fields = tx.select('td')
#     tx_data = {
#         'tx_hash': tx_fields[1].get_text(),
#         'method': tx_fields[2].get_text(),
#         'block': tx_fields[3].get_text(),
#         'time': tx_fields[4].get_text(),
#         'from': tx_fields[6].get_text(),
#         'way': tx_fields[7].get_text(),
#         'to': tx_fields[8].get_text().strip(),
#         'value': tx_fields[9].get_text(),
#         'fee': tx_fields[10].get_text(),
#     }
#     return tx_data
#
#
#
# def get_transactions(wallet):
#     #wallet_link = get_blockchain_wallet_link(wallet)
#     wallet_link = wallet
#     soup = BeautifulSoup(get_page(wallet_link), 'lxml')
#     transactions = soup.find(class_='table table-hover').find('tbody').select('tr')
#     return transactions
#
# txs = get_transactions('https://bscscan.com/address/0x07B49A36b33621edFbA7ccDCE6b96997ea1Ef2e3')
# print(get_tx_data(txs[2]))