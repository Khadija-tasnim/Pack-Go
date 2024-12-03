from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from userprofile.models import UserProfile

def base(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')


        if not uname or not email or not pw1 or not pw2:
            messages.error(request, "All fields are required.")
            return render(request, 'registration/signup.html')

        if pw1 != pw2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/signup.html')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration/signup.html')

        try:

            my_user = User.objects.create_user(username=uname, email=email, password=pw1)
            my_user.save()

            user_profile = UserProfile.objects.create(
                user=my_user,
                full_name=full_name,
                phone_number=phone_number,
                address=address
            )
            user_profile.save()

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the account: {str(e)}")
            return render(request, 'registration/signup.html')

    return render(request, 'registration/signup.html')

def LOGOUT(request):
    logout(request)
    return redirect("home")

def LOGIN(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return render(request, 'userprofile/profile.html',{'username':uname})
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'registration/login.html')