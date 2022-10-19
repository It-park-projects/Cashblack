from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth .decorators import login_required
from register.models import *


def sigin_in(request):
    context = {}
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=='' or password=='':
            context['error'] = "Login yoki parolni kiritmadingiz !"
            return render(request,'register/login.html',context)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('static_information')
        else:
            context['error'] = "Login yoki parol xato !"
    return render(request,'register/login.html',context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('sigin_in')

@login_required
def home_admin(request):
    return render(request,'register/index.html')

@login_required
def static_information(request):
    return render(request,'register/static_information.html')

@login_required
def billling_sistem(request):
    return render(request,'register/billing.html')

@login_required
def all_ctageor(request):
    return render(request,'register/categor.html')