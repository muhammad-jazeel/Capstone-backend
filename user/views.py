from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        re_password = request.POST.get('repassword')
        user_type = request.POST.get('user_type') 

        if password != re_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'auth/signup.html')

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'auth/signup.html')

        if Account.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already registered.")
            return render(request, 'auth/signup.html')
        try:
            user = Account.objects.create_user(
                email=email,
                phone_number=phone_number,
                password=password,
                first_name='',  
                last_name='',
                user_type=user_type
            )
            auth_login(request, user)  
            return redirect('dashboard')  
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'auth/signup.html')
    return render(request, 'auth/signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            if user.user_type == 'vendor':
                return redirect('dashboard')  
            elif user.user_type == 'customer':
                return redirect('customer_dashboard')  
            else:
                messages.error(request, "Invalid user type.")
                return redirect('login')  
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'auth/login.html') 

    return render(request, 'auth/login.html') 

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AccountSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_users(request):
    users = Account.objects.all()
    serializer = AccountSerializer(users, many=True)  
    return Response(serializer.data, status=200)

@login_required
def dashboard_view(request):
    if request.user.user_type != 'vendor':
        messages.error(request, "You do not have permission to access the vendor dashboard.")
        return redirect('home') 

    return render(request, 'vendor/dashboard.html') 

