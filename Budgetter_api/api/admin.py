from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PurchaseCategory, Payment, PaymentDetail, PaymentRecord, Subscription, PaymentGroup

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_superuser')
    ordering = ('email',)
    search_fields = ('email', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Payment)
admin.site.register(PaymentDetail)
admin.site.register(PurchaseCategory)
admin.site.register(PaymentRecord)
admin.site.register(Subscription)
admin.site.register(PaymentGroup)
