import base64
import os
import time
import traceback
from io import BytesIO

import imageio
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import redirect, render
from termcolor import colored

from pyexpat.errors import messages
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from datetime import datetime, timedelta

from termcolor import colored

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
            else:
                mydict['userForm'] = userForm
                return render(request, 'accounts/register.html', mydict)

    return render(request, 'accounts/register.html', mydict)


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
        patients = Patient.objects.all().filter(doctor_id=request.user.doctor)  # show the list
        patients_count = patients.count()
        consultations = Consultation.objects.filter(doctor=request.user.doctor)
        consultations_count = consultations.count()

        mydict = {
            'patients_count': patients_count,
            'consultations_count': consultations_count
        }
        return render(request, 'accounts/dashboard.html', mydict)
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
    user = request.user.doctor
    mydict = {'patientForm': patientForm, 'user': user}
    if request.method == 'POST':
        patientForm = form.PatientForm(request.POST)
        if patientForm.is_valid():
            patientForm = patientForm.save(commit=False)
            patientForm.doctor = request.user.doctor
            patientForm.save()
            messages.success(request, 'New patient was created')
            return redirect('add_patient')
        else:
            mydict['patientForm'] = patientForm
            return render(request, 'accounts/add_patient.html', mydict)
    return render(request, 'accounts/add_patient.html', mydict)


@login_required(login_url='login')
def doctor_list_patients(request):
    patients = Patient.objects.all().filter(doctor_id=request.user.doctor)
    args = {'patients': patients}
    return render(request, 'accounts/doctor_list_patients.html', context=args)


@login_required(login_url='login')
def EditPatient(request, pk):
    patient = Patient.objects.get(id=pk)
    patientForm = form.PatientEditForm(instance=patient)
    mydict = {'patientForm': patientForm}
    if request.method == 'POST':
        patientForm = form.PatientForm(request.POST, instance=patient)
        if patientForm.is_valid():
            patientForm.save()
            return redirect('list_patients')

    return render(request, 'accounts/edit_patient.html', mydict)


@login_required(login_url='login')
def DeletePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    patient.delete()
    return redirect('list_patients')


@login_required(login_url='login')
def AddDirectConsultation(request):
    consultationForm = form.DirectConsultationForm()
    mydict = {'consultationForm': consultationForm}
    if request.method == 'POST':
        consultationForm = form.DirectConsultationForm(request.POST)
        if consultationForm.is_valid():
            consultationForm = consultationForm.save(commit=False)
            consultationForm.doctor = request.user.doctor
            consultationForm.save()
            return redirect('list_consultations')
    return render(request, 'accounts/add_direct_consultation.html', mydict)


@login_required(login_url='login')
def AddConsultation(request, pk):
    consultationForm = form.ConsultationForm()
    patient = Patient.objects.get(id=pk)
    mydict = {'consultationForm': consultationForm, 'patient': patient}
    if request.method == 'POST':
        consultationForm = form.ConsultationForm(request.POST)
        if consultationForm.is_valid():
            consultationForm = consultationForm.save(commit=False)
            consultationForm.doctor = request.user.doctor
            consultationForm.patient = patient
            consultationForm.save()
            return redirect('list_consultations')

    return render(request, 'accounts/add_consultation.html', mydict)


@login_required(login_url='login')
def doctor_list_consultations(request):
    consultation = Consultation.objects.filter(doctor=request.user.doctor).select_related()
    args = {'consultation': consultation}
    return render(request, 'accounts/doctor_list_consultations.html', context=args)


@login_required(login_url='login')
def DeleteConsultation(request, pk):
    consultation = Consultation.objects.get(id=pk)
    consultation.delete()
    return redirect('list_consultations')


@login_required(login_url='login')
def PatientProfile(request, pk):
    patient = Patient.objects.get(id=pk)
    args = {'patient': patient}
    return render(request, 'accounts/patient_profile.html', args)


@login_required(login_url='login')
def EditConsultation(request, pk):
    consultation = Consultation.objects.get(id=pk)
    consultationForm = form.ConsultationForm(instance=consultation)
    mydict = {'consultationForm': consultationForm}
    if request.method == 'POST':
        consultationForm = form.ConsultationForm(request.POST, instance=consultation)
        if consultationForm.is_valid():
            consultationForm.save()
            return redirect('view_consultation', pk)

    return render(request, 'accounts/edit_consultation.html', mydict)


@login_required(login_url='login')
def ConsultationView(request, pk):
    consultation = Consultation.objects.select_related().get(id=pk)
    args = {'consultation': consultation}
    return render(request, 'accounts/view_consultation.html', args)


@login_required(login_url='login')
def images_upload(request, pk):
    consultation = Consultation.objects.get(id=pk)
    ImageForm = form.ImagesForm()
    mydict = {'ImageForm': ImageForm}
    if request.method == 'POST':
        ImageForm = form.ImagesForm(request.POST, request.FILES)
        if ImageForm.is_valid():
            ImageForm = ImageForm.save(commit=False)
            ImageForm.Consultation = consultation
            ImageForm.save()
            return redirect('list_consultations')

    return render(request, 'accounts/add_images.html', mydict)


@login_required(login_url='login')
def ajax_server(request,pk):
    start = time.time()
    d = dict()
    generic = dict()
    medinfo = dict()
    images = Images.objects.get(id=pk)
    try:
        if  str(images.Image_Consultation)[-3:].upper() =='DCM':
            filename = str(images.Image_Consultation)[max(index for index, item in enumerate(str(images.Image_Consultation)) if item == '/')+1:]
            full_path_file = str(images.Image_Consultation)

            generic['name'] = filename
            generic['size'] = os.path.getsize(full_path_file)
            try:
                if full_path_file[-3:].upper() == 'DCM':
                    dcpimg = imageio.imread(full_path_file)
                    for keys in dcpimg.meta:

                        medinfo[keys] = str(dcpimg.meta[keys])

                    if len(dcpimg.shape) ==4:
                        dcpimg = dcpimg[0,0]
                    elif len(dcpimg.shape) ==3:
                        dcpimg = dcpimg[0]

                    fig = plt.gcf()
                    fig.set_size_inches(18.5, 10.5)
                    plt.imshow(dcpimg, cmap='gray')
                    plt.colorbar()
                    figure = BytesIO()
                    plt.savefig(figure, format='jpg', dpi=300)

                    plt.close()
                    d['url'] = {'base64': 'data:image/png;base64,' + base64.b64encode(figure.getvalue()).decode()}

            except Exception as e:

                traceback.print_tb(e)


    except Exception as e:
        traceback.print_tb(e)
    mydict = {'d': d}
    #return JsonResponse(d)
    return render(request, 'accounts/show_images.html', mydict)



