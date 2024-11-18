from django.shortcuts import render

def staffs_view(request):
    return render(request, 'vendor/staff/staff.html')  

def add_staff_view(request):
    return render(request, 'vendor/staff/add_staff.html')

def edit_staff_view(request):
    return render(request, 'vendor/staff/edit_staff.html')


def delete_staff_view(request):
    return render(request, 'vendor/staff/delete_staff.html')
