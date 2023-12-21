from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Logged Out Successfully')
            form.save()
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form, 'type': 'Register'})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=name, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('profile')
            else:
                messages.warning(request, 'Login informtion incorrect')
                return redirect('register')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'type': 'Log In'})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('home')


def profile(request):
    return render(request, 'profile.html')


def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Update Succesfully")
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_pass.html', {'form': form, 'type': 'Change Password'})
