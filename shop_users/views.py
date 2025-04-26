from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('shop_users:login')
    else:
        form = UserCreationForm()
    return render(request, 'shop_users/register.html', {'form': form})

@login_required
def profile(request):
    """View for user profile"""
    return render(request, 'shop_users/profile.html')