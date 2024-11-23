from datetime import datetime, time
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Service, Department
from staff.models import *
from .forms import ServiceForm  
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def add_services_view(request):
    if request.method == 'POST':
        name = request.POST.get('serviceName')
        price = request.POST.get('servicePrice')
        duration_minutes = request.POST.get('serviceDuration')
        start_time = request.POST.get('startTime')
        end_time = request.POST.get('endTime')
        description = request.POST.get('serviceDescription')
        selected_staff_ids = request.POST.getlist('selectedStaffs')  


        if not name or not price or not duration_minutes or not start_time or not end_time or not description:
            messages.error(request, "All fields except 'Staff Assigned' are required.")
            return redirect('add_services_view')

        try:
            service = Service.objects.create(
                name=name,
                description=description,
                price=float(price),
                duration_minutes=int(duration_minutes),
                start_time=start_time,
                end_time=end_time,
                user=request.user,
            )

            for staff_id in selected_staff_ids:
                staff = Staff.objects.filter(id=staff_id, user=request.user).first()
                if staff:
                    StaffServiceAssignment.objects.create(staff=staff, service=service)

            messages.success(request, f"Service '{service.name}' added successfully!")
            return redirect('services')
        except Exception as e:
            messages.error(request, f"Error adding service: {e}")
            return redirect('add_services_view')

    staffs = Staff.objects.filter(user=request.user)
    return render(request, 'vendor/service/add_services.html', {'staffs': staffs})

@login_required
def edit_service_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')
        status = request.POST.get('status')
        selected_staff_ids = request.POST.getlist('staffs')
        removed_slots = request.POST.getlist('removed_slots') 

        if not name or not price or not duration_minutes or not start_time or not end_time or not description:
            messages.error(request, "All fields are required except 'Image'.")
            return redirect('edit_service_view', service_id=service_id)

        try:
            service.name = name
            service.price = price
            service.duration_minutes = duration_minutes
            service.start_time = start_time
            service.end_time = end_time
            service.description = description
            service.status = status
            service.save()

            StaffServiceAssignment.objects.filter(service=service).delete() 
            for staff_id in selected_staff_ids:
                staff = Staff.objects.filter(id=staff_id, user=request.user).first()
                if staff:
                    StaffServiceAssignment.objects.create(service=service, staff=staff)

            if removed_slots:
                for slot in removed_slots:
                    slot_time = datetime.strptime(slot, "%H:%M").time()
                    service.slots.filter(slot_time=slot_time).delete()

            messages.success(request, f"Service '{service.name}' updated successfully!")
            return redirect('services')
        except Exception as e:
            messages.error(request, f"Error updating service: {e}")
            return redirect('edit_service_view', service_id=service_id)

    else:
        assigned_staff_ids = StaffServiceAssignment.objects.filter(service=service).values_list('staff_id', flat=True)
        staffs = Staff.objects.filter(user=request.user)

        slots = service.calculate_slots()

    return render(
        request,
        'vendor/service/edit_services.html',
        {
            'service': service,
            'staffs': staffs,
            'assigned_staff_ids': assigned_staff_ids,
            'slots': slots,
        }
    )

@login_required
def delete_service_view(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)
    if request.method == 'POST':
        StaffServiceAssignment.objects.filter(service=service).delete()  
        service.delete()
        messages.success(request, f"Service '{service.name}' deleted successfully!")
        return redirect('services')
    return render(request, 'vendor/service/delete_services.html', {'service': service})



# @login_required
# def services_view(request):
#     """
#     Display the list of services created by the logged-in vendor.
#     Includes search and filter options.
#     """
#     user = request.user

#     services = Service.objects.filter(user=user)

#     search_query = request.GET.get('search', '').strip()
#     filter_department = request.GET.get('department', '').strip()
#     filter_status = request.GET.get('status', '').strip()

#     if search_query:
#         services = services.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )

#     if filter_department:
#         services = services.filter(department__id=filter_department)

#     if filter_status:
#         services = services.filter(status=filter_status)

#     departments = user.departments.all() 

#     context = {
#         'services': services,
#         'departments': departments,
#         'search_query': search_query,
#         'filter_department': filter_department,
#         'filter_status': filter_status,
#     }
#     return render(request, 'vendor/service/services.html', context)

@login_required
def services_view(request):
    search_query = request.GET.get('search', '').strip()
    services = Service.objects.filter(user=request.user)

    if search_query:
        services = services.filter(name__icontains=search_query)

    return render(request, 'vendor/service/services.html', {
        'services': services
    })



