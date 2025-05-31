from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, 
    Payment, 
    PaymentDetail, 
    Category, 
    CategoryDetail, 
    PaymentRecord, 
    Subscription, 
    LoanRecord
)

AdminSite.site_header = 'Budgetter管理画面'
AdminSite.site_title = 'サイト管理者'
AdminSite.index_title = 'サイト管理'

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
admin.site.register(Category)
admin.site.register(CategoryDetail)
admin.site.register(PaymentRecord)
admin.site.register(Subscription)
admin.site.register(LoanRecord)