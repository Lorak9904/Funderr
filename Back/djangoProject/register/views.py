from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from django.utils import timezone
from .forms import RegisterForm
# from .models import Employee, RegistrationKey
import uuid


def check_key(request):
    # if request.method == "POST":
    #     key_value = request.POST.get('key', '').strip()

    #     try:
    #         # Check if the key exists and is valid
    #         reg_key = RegistrationKey.objects.get(key=key_value)
    #         if reg_key.is_valid() and not reg_key.is_used:
    #             # Render the registration form after key is verified
    #             form = RegisterForm()  # Form initialized here after key validation
    #             return render(request, 'register/register.html', {
    #                 'form': form,
    #                 'company': reg_key.company, 
    #                 'key': key_value  # Pass the key as string
    #             })
    #         else:
    #             return render(request, 'register/key_input.html', {
    #                 'error': 'Key is invalid, expired, or already used'
    #             })
    #     except RegistrationKey.DoesNotExist:
    #         return render(request, 'register/key_input.html', {
    #             'error': 'Key not found'
    #         })

    return render(request, 'register/key_input.html')

def register(request):
    # if request.method == "POST":
    #     # Check if it's the key verification form
    #     form_type = request.POST.get('form_type', '')
        
    #     if form_type == 'check_key_form':
    #         key_value = request.POST.get('key', '').strip()
    #         try:
    #             reg_key = RegistrationKey.objects.filter(key=key_value).first()
                
    #             if reg_key:
    #                 form = RegisterForm()
    #                 return render(request, 'register/register.html', {
    #                     'form': form,
    #                     'company': reg_key.company,
    #                     'key': reg_key
    #                 })
    #             else:
    #                 return render(request, 'register/key_input.html', {
    #                     'error': 'Key not found or invalid'
    #                 })
    #         except ValidationError:
    #             return render(request, 'register/key_input.html', {
    #                 'error': 'Key not found or invalid'
    #             })

    #     # Check if it's the registration form
    #     elif form_type == 'registration_form':
    #         form = RegisterForm(request.POST)
    #         key_value = request.POST.get('key', '').strip()
    #         reg_key = RegistrationKey.objects.filter(key=key_value).first()

    #         if form.is_valid() and reg_key:
    #             user = form.save()
    #             company = reg_key.company
    #             Employee.objects.create(user=user, company=company)
    #             user.save()

    #             # Mark the key as used
    #             reg_key.is_used = True
    #             reg_key.save()

    #             return redirect('/')  # Redirect to a success page after registration
    #         else:
    #             return render(request, 'register/register.html', {
    #                 'form': form,
    #                 'error': 'Form invalid or key not found',
    #                 'key': reg_key
    #             })
    
    return render(request, 'register/key_input.html')
    






# def register(request):
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             company = form.cleaned_data.get('company').lower() 
#             Employee.objects.create(user=user, company=company)
#             return redirect('/')
#     else:
#         form = RegisterForm()
#     return render(request, 'register/register.html', {'form': form})
