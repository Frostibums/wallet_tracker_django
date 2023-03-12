from django.contrib import messages
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('login')
    else:
        register_form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': register_form})

def login(request):
    return render(request, 'users/login.html')

def logout(request):
    return render(request, 'users/logout.html', {'message': f'logged out'})

