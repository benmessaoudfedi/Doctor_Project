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

    def clean(self):

        # data from the form is fetched using super function
        super(CreateUserForm, self).clean()

        # extract the username and text field from the data
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        # conditions to be met for the username length
        if len(username) < 5:
            raise forms.ValidationError({"username": "not valid user name"})
        if (len(p1) or len(p2)) < 8:
            raise forms.ValidationError({"password1": "'not valid user password'"})
        if p1 != p2:
            raise forms.ValidationError({"password2": "passwods not much"})
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email exists")
        # return any errors if found
        return self.cleaned_data

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
    def clean(self):

        # data from the form is fetched using super function
        super(PatientForm, self).clean()

        # extract the username and text field from the data
        carte_cin = self.cleaned_data.get('carte_cin')
        # conditions to be met for the username length
        if len(str(carte_cin)) != 8 or not(str(carte_cin).isdigit()):
            raise forms.ValidationError({"carte_cin": "Invalid CIN, 8 Digits "})
        return self.cleaned_data



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

class ImagesForm(forms.ModelForm):
    class Meta:
        model = models.Images
        fields = ['Image_Consultation', 'model_image']
        exclude=['Consultation']