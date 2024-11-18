from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def dashboard_view(request):
    if request.user.user_type != 'vendor':
        messages.error(request, "You do not have permission to access the vendor dashboard.")
        return redirect('home') 

    return render(request, 'vendor/dashboard.html') 