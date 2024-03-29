from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'user/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            login(request, user)
            return redirect('login')
    return render(request, 'user/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def password_reset_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('comfirm_password')
        if new_password != confirm_password:
            messages.error(request, 'Password does not match.')
        
        user = authenticate(request, username=request.user.username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Invalid password.')