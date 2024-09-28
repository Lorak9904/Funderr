from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Firma, NGO, Konkurs

# class EmployeeInline(admin.StackedInline):
#     model = Firma
#     can_delete = False
#     verbose_name_plural = "Firma"

# class UserAdmin(BaseUserAdmin):
#     inlines = [EmployeeInline]
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'company')  # Add 'company' to list_display
#     list_select_related = ('employee',)  # Optimizes queries by using select_related

#     def company(self, obj):
#         return obj.employee.company  # Access the related Employee model

#     company.admin_order_field = 'employee__company'  # Enable sorting by company
#     company.short_description = 'Company'

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.annotate(company_name=F('employee__company'))
#         return queryset


# class NGOAdmin(admin.ModelAdmin):
#     list_display = ('key', 'company', 'created_at', 'is_used')
#     list_filter = ('company', 'is_used', 'created_at')
#     search_fields = ('key', 'company__companyName')

#     def company(self, obj):
#         return obj.company.companyName  

#     company.admin_order_field = 'company'  
#     company.short_description = 'Company'  



admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Firma)
admin.site.register(NGO)
# admin.site.register(Konkurs)




from django.contrib import admin
from .models import Konkurs, Priorytet, Zadanie, Terminy, ZasadyDotacji, Partner

# Inline model for Priorytet related to Konkurs
class PriorytetInline(admin.TabularInline):
    model = Priorytet
    extra = 1  # Number of empty forms to display

# Inline model for Terminy related to Konkurs
class TerminyInline(admin.StackedInline):
    model = Terminy
    can_delete = False  # Terminy is one-to-one, so can only have one instance per Konkurs

# Inline model for ZasadyDotacji related to Konkurs
class ZasadyDotacjiInline(admin.StackedInline):
    model = ZasadyDotacji
    can_delete = False

# Admin for Konkurs with inlines
class KonkursAdmin(admin.ModelAdmin):
    inlines = [PriorytetInline, TerminyInline, ZasadyDotacjiInline]
    list_display = ('nazwa', 'data_ogloszenia', 'data_zakonczenia_skladania_ofert', 'calkowita_kwota')
    search_fields = ('nazwa', 'opis')
    list_filter = ('data_ogloszenia', 'data_zakonczenia_skladania_ofert')

# Register other models individually
admin.site.register(Konkurs, KonkursAdmin)
admin.site.register(Zadanie)  # Zadanie is managed separately under Priorytet
admin.site.register(Partner)
