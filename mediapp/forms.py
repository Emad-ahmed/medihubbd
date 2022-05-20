from cProfile import label
from django.forms import widgets
from mediapp.models import Customer, DoctorInfo, Product,  Ambulanceadd
from typing import Set
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from mediapp.models import UploadPrescription


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'autofocus': True, 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city',  'zipcode']
        labels = {'zipcode': 'Postal Code'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UploadPrescriptionForm(forms.ModelForm):
    class Meta:
        model = UploadPrescription
        fields = ['prescription_image']
        widgets = {
            'prescription_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DoctorInfoForm(forms.ModelForm):
    class Meta:
        model = DoctorInfo
        fields = ['name', 'qualification', 'specialist', 'chamber',
                  'chamber_address', 'serial_number', 'visiting_hour', 'new_patient_fee', 'old_patient_fee', 'report_checking_fee', 'doctor_img', 'city']
        labels = {'name': 'Full Name', 'new_patient_fee': 'Patient Fee'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialist': forms.TextInput(attrs={'class': 'form-control'}),
            'chamber': forms.TextInput(attrs={'class': 'form-control'}),
            'chamber_address': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'visiting_hour': forms.TextInput(attrs={'class': 'form-control'}),
            'new_patient_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'old_patient_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'report_checking_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'doctor_img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'cattype', 'selling_price', 'discounted_price',
                  'description', 'Disclaimer', 'brand', 'category', 'product_image']
        labels = {'cattype': 'Category Type'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'cattype': forms.TextInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'Disclaimer': forms.Textarea(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }


class AddAmbulaceForm(forms.ModelForm):
    class Meta:
        model = Ambulanceadd
        fields = ['service_name', 'service_phone', 'state']

        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control'}),
            'service_phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),

        }
