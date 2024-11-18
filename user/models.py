from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None, user_type=None):
        if not email:
            raise ValueError('User must have an email address')
        if not phone_number:
            raise ValueError('User must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type
        )
        user.set_password(password)

        if user_type == 'customer':
            user.is_customer = True
        elif user_type == 'vendor':
            user.is_vendor = True

        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            user_type='admin'
        )
        user.is_vendor = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    groups = models.ManyToManyField(Group, related_name='accounts', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='accounts', blank=True)

class Vendor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_license = models.CharField(max_length=255)
    verification_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name
