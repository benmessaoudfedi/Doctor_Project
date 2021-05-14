from pyexpat.errors import messages
from django.contrib.auth.models import Group

from django.shortcuts import render, redirect

from Doctor.form import CreateUserForm
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
                doctor = doctor.save()
                my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
                my_doctor_group[0].user_set.add(user)
            return redirect('login')
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

