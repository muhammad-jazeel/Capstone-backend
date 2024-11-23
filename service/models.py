from django.db import models
from department.models import *
from datetime import date, datetime, timedelta
from django.db import models
from user.models import *

class Service(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    start_time = models.TimeField(null= True)
    end_time = models.TimeField(null= True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="services", null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="services", null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def calculate_slots(self):
        if not self.start_time or not self.end_time or not self.duration_minutes:
            return []

        slots = []
        current_time = self.start_time
        delta = timedelta(minutes=self.duration_minutes)

        while current_time < self.end_time:
            slots.append(current_time)
            current_time = (datetime.combine(date.today(), current_time) + delta).time()

        return slots



class BookingSlot(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="slots")
    slot_time = models.TimeField()  
    is_booked = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.slot_time}"



