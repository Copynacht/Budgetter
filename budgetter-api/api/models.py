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
    icon = models.CharField(max_length=255, default='mdi-credit-card', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                condition=models.Q(is_active=True),
                name='unique_active_name'
            )
        ]

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.payment.name})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['payment', 'name'],
                condition=models.Q(is_active=True),
                name='unique_active_payment_name'
            )
        ]

class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=255, default='mdi-information-outline', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                condition=models.Q(is_active=True),
                name='unique_active_user_name'
            )
        ]

class CategoryDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                condition=models.Q(is_active=True),
                name='unique_active_category_name'
            )
        ]


class PaymentRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='record')
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    price = models.IntegerField(default=0)
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.SET_NULL)
    payment_detail = models.ForeignKey(PaymentDetail, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    category_detail = models.ForeignKey(CategoryDetail, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscription')
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    payment = models.ForeignKey(Payment, null=True, blank=True, on_delete=models.SET_NULL)
    payment_detail = models.ForeignKey(PaymentDetail, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    category_detail = models.ForeignKey(CategoryDetail, null=True, blank=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"

class LoanRecord(models.Model):
    LOAN_TYPE_CHOICES = [
        (0, '貸した'),
        (1, '借りた'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='loan_records')
    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, blank=True)
    price = models.IntegerField(default=0)
    loan_type = models.IntegerField(choices=LOAN_TYPE_CHOICES)
    date = models.DateField(auto_now_add=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_loan_type_display()} {self.name} - {self.price}円"

