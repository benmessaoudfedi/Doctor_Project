from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Doctor import models


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()

        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'email']


class PatientForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = '__all__'
        exclude=['doctor','doctors']

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ['first_name', 'last_name', 'address', 'date_naissance', 'mobile', 'carte_cin', 'sexe', 'type_dossier', 'provenance']

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = models.Consultation
        fields = '__all__'
        exclude=['doctor', 'patient']

class DirectConsultationForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=models.Patient.objects.all(),empty_label="Patient Name")
    class Meta:
        model = models.Consultation
        fields = '__all__'
        exclude=['doctor']

