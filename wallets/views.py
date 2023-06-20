from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .services import get_user_wallets, remove_wallet_from_user, get_wallet_owner, update_wallet_txs, get_wallet_txs
from wallets.forms import WalletAddForm


@login_required
def wallets_with_txs_list(request):
    all_txs = []
    wallets = get_user_wallets(request.user)
    for wallet in wallets:
        #update_wallet_txs(wallet)
        wallet_txs = get_wallet_txs(wallet, 5)
        all_txs.append(wallet_txs)
    context = {
        'all_txs': all_txs,
    }
    return render(request, 'wallets/wallets_with_txs_list.html', context)


@login_required
def add_wallet(request):
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
            update_wallet_txs(new_wallet)
            return redirect('wallets_list')
    else:
        wallet_add_form = WalletAddForm()
    return render(request, 'wallets/add.html', {'form': wallet_add_form})


@login_required
def remove_wallet(request, wallet_address):
    if request.user == get_wallet_owner(wallet_address):
        remove_wallet_from_user(wallet_address)
        messages.success(request, f'Кошелек удален!')
        return redirect('wallets_list')
    messages.error(request, f'Данный кошелек не пренадлежит вам! {wallet_address}')
    return redirect('wallets_list')


@login_required
def wallets_list(request):
    wallets = get_user_wallets(request.user)
    return render(request, 'wallets/list.html', {'wallets': wallets})