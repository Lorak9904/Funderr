from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import F
from .models import Employee, Company, RegistrationKey

class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = "Employee"

class UserAdmin(BaseUserAdmin):
    inlines = [EmployeeInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'company')  # Add 'company' to list_display
    list_select_related = ('employee',)  # Optimizes queries by using select_related

    def company(self, obj):
        return obj.employee.company  # Access the related Employee model

    company.admin_order_field = 'employee__company'  # Enable sorting by company
    company.short_description = 'Company'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(company_name=F('employee__company'))
        return queryset


class RegistrationKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'company', 'created_at', 'is_used')
    list_filter = ('company', 'is_used', 'created_at')
    search_fields = ('key', 'company__companyName')

    def company(self, obj):
        return obj.company.companyName  

    company.admin_order_field = 'company'  
    company.short_description = 'Company'  



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Company)
admin.site.register(RegistrationKey, RegistrationKeyAdmin)
