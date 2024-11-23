from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from service.models import Service
from staff.models import Staff
from department.models import Department

@login_required
def dashboard_view(request):
    if request.user.user_type != 'vendor':
        messages.error(request, "You do not have permission to access the vendor dashboard.")
        return redirect('home')

    total_services = Service.objects.filter(user=request.user).count()  
    total_staff = Staff.objects.filter(user=request.user).count()
    active_departments = Department.objects.filter(
        created_by=request.user, status='active'
    ).count()       

    return render(request, 'vendor/dashboard.html', {
        'total_services': total_services,
        'total_staff': total_staff,
        'active_departments': active_departments,
    })
