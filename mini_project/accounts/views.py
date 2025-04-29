from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse

from accounts.models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.core.mail import send_mail
import random

def Get_Started(request):
    return render(request, 'Get_Started.html')

def home(request):
    return render(request, 'home.html')

def login_signup(request):
    login_form = CustomAuthenticationForm()
    registration_form = CustomUserCreationForm()
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        elif 'signup' in request.POST:
            registration_form = CustomUserCreationForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('home')
            else:
                messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, 'login_signup.html', {'login_form': login_form, 'registration_form': registration_form})

def Otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        request.session['otp'] = otp
        request.session['email'] = email
        # Replace with actual email sending logic
        send_mail('Your OTP Code', f'Your OTP is {otp}', 'from@example.com', [email])
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_otp')
    return render(request, 'Otp.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_input = ''.join([request.POST.get(f'otp{i}') for i in range(1, 5)])
        if otp_input == request.session.get('otp'):
            email = request.session.get('email')
            request.session['verified_email'] = email
            messages.success(request, "OTP verified.")
            return redirect('reset_password_form')
        else:
            messages.error(request, "Invalid OTP.")
    return render(request, 'verify_otp.html')

def reset_password_form(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password == confirm_password:
            email = request.session.get('verified_email')
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successful.")
            return redirect('home')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'reset_password_form.html')

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
