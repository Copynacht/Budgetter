from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=255, unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.payment.name})"

class PurchaseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class PaymentRecord(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(PurchaseCategory, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    payment_detail = models.ForeignKey(PaymentDetail, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Subscription(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(PurchaseCategory, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    payment_detail = models.ForeignKey(PaymentDetail, null=True, blank=True, on_delete=models.SET_NULL) 
    order = models.PositiveIntegerField(default=0)   
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

class PaymentGroup(models.Model):
    name = models.CharField(max_length=255)
    payments = models.ManyToManyField(Payment, blank=True)
    payment_details = models.ManyToManyField(PaymentDetail, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
