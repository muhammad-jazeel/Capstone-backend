from django.shortcuts import render, redirect
from .models import Department
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def departments_view(request): 
    return render(request, 'vendor/department/department.html')

@login_required
def add_department_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')  

        if not name:  
            messages.error(request, "Department name cannot be empty.")
            return render(request, 'vendor/department/add_department.html')

        if Department.objects.filter(name=name, created_by=request.user).exists():
            messages.error(request, "A department with this name already exists.")
            return render(request, 'vendor/department/add_department.html')

        Department.objects.create(name=name, created_by=request.user)
        messages.success(request, f"Department '{name}' added successfully!")

        return redirect('departments')

    return render(request, 'vendor/department/add_department.html')


def edit_department_view(request):
    return render(request, 'vendor/department/edit_department.html')


def delete_department_view(request):
    return render(request, 'vendor/department/delete_department.html')

