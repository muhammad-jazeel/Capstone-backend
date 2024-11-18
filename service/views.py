from django.shortcuts import render

def services_view(request):
    return render(request, 'vendor/services.html')

def add_services_view(request):
    return render(request, 'vendor/add_services.html')