from pyexpat.errors import messages
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm

from Doctor import form


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.

from Doctor.decorators import allowed_user, unauthenticated_user


def accueil(request):
    return render(request, 'accounts/Home.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/home')
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin')
    else:
        userForm = form.CreateUserForm()
        doctorForm = form.DoctorForm()
        mydict = {'userForm': userForm, 'doctorForm': doctorForm}
        if request.method == 'POST':
            userForm = form.CreateUserForm(request.POST)
            doctorForm = form.DoctorForm(request.POST, request.FILES)
            if userForm.is_valid() and doctorForm.is_valid():
                user = userForm.save()
                user.save()
                usermes = userForm.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + usermes)
                doctor = doctorForm.save(commit=False)
                doctor.user = user
                doctor.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
            return redirect('login')

    mydict = {'userForm': userForm, 'doctorForm': doctorForm}

    return render(request, 'accounts/register.html', context=mydict)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    accountapproval = Doctor.objects.all().filter(user_id=request.user.id, status=True)
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('/admin')
    elif request.user.is_authenticated and accountapproval:
        return render(request, 'accounts/dashboard.html')
    else:
        return render(request, 'accounts/doctor_wait_for_approval.html')


@login_required(login_url='login')
def profileview(request):
    args = {'user': request.user}
    return render(request, 'accounts/profileview.html', args)


@login_required(login_url='login')
def profileedit(request):
    userForm = form.EditProfileForm(instance=request.user)
    doctorForm = form.DoctorForm(instance=request.user.doctor)
    if request.method == 'POST':
        userForm = form.EditProfileForm(request.POST, instance=request.user)
        doctorForm = form.DoctorForm(request.POST, request.FILES, instance=request.user.doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.save()
        return redirect('/profile/edit')
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    return render(request, 'accounts/profileedit.html', context=mydict)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profileview'))
        else:
            return redirect(reverse('change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


@login_required(login_url='login')
def AddPatient(request):
    patientForm = form.PatientForm()
    user=request.user.doctor
    mydict = {'patientForm': patientForm,'user':user}
    if request.method == 'POST':
        patientForm = form.PatientForm(request.POST)
        if patientForm.is_valid():
            patientForm= patientForm.save(commit=False)
            patientForm.doctor=request.user.doctor
            patientForm.save()
            return redirect('add_patient')

    return render(request, 'accounts/add_patient.html', mydict)


@login_required(login_url='login')
def doctor_list_patients(request):
    patients=Patient.objects.all().filter(doctor_id=request.user.doctor)
    args = {'patients': patients}
    return render(request,'accounts/doctor_list_patients.html',context=args)


@login_required(login_url='login')
def EditPatient(request,pk):
    patient= Patient.objects.get(id=pk)
    patientForm = form.PatientEditForm(instance=patient)
    mydict = {'patientForm': patientForm}
    if request.method == 'POST':
        patientForm = form.PatientForm(request.POST, instance=patient)
        if patientForm.is_valid():
            patientForm.save()
            return redirect('list_patients')

    return render(request, 'accounts/edit_patient.html', mydict)\

@login_required(login_url='login')
def DeletePatient(request,pk):
    patient= Patient.objects.get(id=pk)
    patient.delete()
    return redirect('list_patients')