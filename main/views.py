from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserProfileForm  # Import the form
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def show_register(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Ensure password is properly set and hashed
            user.set_password(form.cleaned_data["password"])

            # Check if age is valid (optional)
            if not user.is_age_valid():
                messages.error(request, "Usia minimal 12 tahun.")
                return render(request, "register.html", {"form": form})

            user.save()  # Save the user in the database
            login(request, user)  # Log in the user automatically
            messages.success(request, f"Registrasi berhasil! Selamat datang, {user.username}")
            print(f"Registrasi berhasil! Selamat datang, {user.username}")

            return redirect("main:login_view")  # Redirect to login page

        else:
            print("gagal")
            print(form.errors) 
            messages.error(request, "Form tidak valid, periksa kembali data Anda.")

    else:
        form = UserProfileForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("masuk home")
            return redirect("main:home")  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("main:login_view")  # Redirect to login page


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile  # Ensure this matches your model

# @login_required
def home_view(request):
    users = UserProfile.objects.all()  # Fetch all users
    return render(request, "home.html", {"users": users})