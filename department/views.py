from django.shortcuts import get_object_or_404, render, redirect
from .models import Department
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def departments_view(request):
    departments = Department.objects.filter(created_by=request.user)
    return render(request, 'vendor/department/department.html', {'departments': departments})

@login_required
def add_department_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Department name cannot be empty.", extra_tags="error")
            return render(request, 'vendor/department/add_department.html')
        
        if Department.objects.filter(name=name, created_by=request.user).exists():
            messages.error(request, "A department with this name already exists.", extra_tags="error")
            return render(request, 'vendor/department/add_department.html')
        
        Department.objects.create(name=name, created_by=request.user)
        messages.success(request, f"Department '{name}' added successfully!", extra_tags="success")
        return redirect('departments')
    return render(request, 'vendor/department/add_department.html')


@login_required
def edit_department_view(request, department_id):
    department = get_object_or_404(Department, id=department_id, created_by=request.user)  

    if request.method == 'POST':
        name = request.POST.get('name') 

        if not name:
            messages.error(request, "Department name cannot be empty.")
            return render(request, 'vendor/department/edit_department.html', {'department': department})

        department.name = name
        department.save()
        messages.success(request, f"Department '{name}' updated successfully!")
        return redirect('departments')  

    return render(request, 'vendor/department/edit_department.html', {'department': department})


@login_required
def delete_department_view(request, department_id):
    department = get_object_or_404(Department, id=department_id, created_by=request.user) 

    if request.method == 'POST':
        department_name = department.name 
        department.delete()
        messages.success(request, f"Department '{department_name}' deleted successfully!")
        return redirect('departments') 

    return render(request, 'vendor/department/delete_department.html', {'department': department})

@login_required
def toggle_department_status(request, department_id):
    department = get_object_or_404(Department, id=department_id, created_by=request.user)

    if department.status == 'active':
        department.set_inactive()
        messages.success(request, f"Department '{department.name}' and its services have been set to inactive.")
    else:
        department.status = 'active'
        department.save()
        messages.success(request, f"Department '{department.name}' has been set to active.")

    return redirect('departments')

