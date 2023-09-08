from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from wallets.forms import WalletAddForm

from .services import get_user_wallets, get_wallet_owner, get_wallet_txs, remove_wallet_from_user
from .tasks import update_wallet_txs


@login_required
def wallets_with_txs_list(request):
    """View for displaying a list of user wallets along with their recent transactions."""
    all_txs = []
    wallets = get_user_wallets(request.user)
    for wallet in wallets:
        wallet_txs = get_wallet_txs(wallet, 5)
        all_txs.append(wallet_txs)
    context = {
        'all_txs': all_txs,
    }
    return render(request, 'wallets/wallets_with_txs_list.html', context)


@login_required
def add_wallet(request):
    """View for adding a new wallet to the user's account."""
    if request.method == 'POST':
        wallet_add_form = WalletAddForm(request.POST)
        if all([wallet_add_form.is_valid(),
                wallet_add_form.validate(),
                ]):
            new_wallet = wallet_add_form.save(commit=False)
            new_wallet.owner = request.user
            new_wallet.save()
            blockchain = request.POST.getlist('blockchains')
            new_wallet.blockchains.add(*blockchain)
            messages.success(request, f'Добавлен кошелек {new_wallet}!')
            update_wallet_txs.delay(new_wallet.wallet_address)
            return redirect('wallets_list')
    else:
        wallet_add_form = WalletAddForm()
    return render(request, 'wallets/add.html', {'form': wallet_add_form})


@login_required
def remove_wallet(request, wallet_address: str):
    """View for removing a wallet from the user's account."""
    if request.user != get_wallet_owner(wallet_address):
        raise PermissionError(f'{request.user} | remove_wallet | {wallet_address}')
    remove_wallet_from_user(wallet_address)
    messages.success(request, 'Кошелек удален!')
    return redirect('wallets_list')


@login_required
def wallets_list(request):
    """View for displaying a list of user wallets."""
    wallets = get_user_wallets(request.user)
    return render(request, 'wallets/list.html', {'wallets': wallets})
