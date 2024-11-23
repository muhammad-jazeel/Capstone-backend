from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Staff
from department.models import Department
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def staffs_view(request):
    
    departments = Department.objects.filter(created_by=request.user)

    search_query = request.GET.get('search', '').strip()
    selected_departments = request.GET.getlist('departments')

    staffs = Staff.objects.filter(user=request.user)

    if search_query:
        staffs = staffs.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if selected_departments:
        staffs = staffs.filter(departments__id__in=selected_departments).distinct()

    context = {
        'staffs': staffs,
        'departments': departments,
    }
    return render(request, 'vendor/staff/staff.html', context)

@login_required
def add_staff_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        department_ids = request.POST.getlist('departments')

        if Staff.objects.filter(email=email).exists():
            messages.error(request, "A staff member with this email already exists.", extra_tags="error")
            return redirect('add_staff')

        if Staff.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "A staff member with this phone number already exists.", extra_tags="error")
            return redirect('add_staff')

        staff = Staff.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
        )

        departments = Department.objects.filter(id__in=department_ids)
        staff.departments.set(departments)

        messages.success(request, f"Staff member '{staff.first_name} {staff.last_name}' added successfully!", extra_tags="success")
        return redirect('staffs')

    departments = Department.objects.filter(created_by=request.user)  
    return render(request, 'vendor/staff/add_staff.html', {'departments': departments})


@login_required
def edit_staff_view(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id, user=request.user)

    if request.method == 'POST':
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.email = request.POST.get('email')
        staff.phone_number = request.POST.get('phone_number')
        department_ids = request.POST.getlist('departments')

        staff.departments.set(Department.objects.filter(id__in=department_ids))
        staff.save()

        messages.success(request, f"Staff member '{staff.first_name} {staff.last_name}' updated successfully!")
        return redirect('staffs')

    departments = Department.objects.filter(created_by=request.user)
    return render(request, 'vendor/staff/edit_staff.html', {'staff': staff, 'departments': departments})


@login_required
def delete_staff_view(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id, user=request.user)

    if request.method == 'POST':
        staff_name = f"{staff.first_name} {staff.last_name}"
        staff.delete()
        messages.success(request, f"Staff member '{staff_name}' deleted successfully!")
        return redirect('staffs')

    return render(request, 'vendor/staff/delete_staff.html', {'staff': staff})

