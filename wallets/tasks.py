from wallet_tracker.celery import app
from wallets.parser import get_new_txs
from wallets.services import get_wallet_blockchains, get_last_block, add_tx_to_wallet, get_all_wallets_addresses, \
    get_wallet


@app.task
def update_wallet_txs(wallet_address, amount=10):
    wallet_txs = {}
    wallet = get_wallet(wallet_address)
    for blockchain in get_wallet_blockchains(wallet):
        start_block = get_last_block(wallet, blockchain)
        wallet_txs[blockchain] = get_new_txs(wallet, blockchain, amount, start_block)
        if wallet_txs.get(blockchain, False):
            for tx in wallet_txs.get(blockchain):
                if int(tx.get('value')):
                    add_tx_to_wallet(wallet, tx, blockchain)
    return True


@app.task
def update_all_wallets_txs():
    wallets = get_all_wallets_addresses()
    for wallet in wallets:
        update_wallet_txs(wallet)
    return True
