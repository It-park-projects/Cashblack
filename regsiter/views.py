from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth .decorators import login_required
from django.views.generic.edit import UpdateView,CreateView
from django.views.generic import ListView,DeleteView,DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from regsiter.models import *
from regsiter.forms import *
from billing.models import *

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
    context = {}
    context['objects_list'] = Shops.objects.all()
    return render(request,'register/static_information.html',context)

@login_required
def billling_sistem(request):
    context = {}
    context['obejcts_list'] = Shops.objects.all()
    return render(request,'register/billing.html',context)

class CreateSummPayment(UpdateView):
    model = Shops
    form_class = ShopsPaymentSumm
    template_name = 'register/biling_summ.html'
    success_url = reverse_lazy('billing_sistem')

@login_required
def create_summ_shops(request):
    context = {}
    if request.method=='POST':
        summ = request.POST.get('summ')
        if summ=='':
            context['error'] = "Summa kiritilmadi"
            return render(request,'register/summ.html',context)
        context['shops'] = Shops.objects.all().update(payment_summ=summ)
        # context['shops'].save()
        return redirect('billing_sistem')
    return render(request,'register/summ.html',context)

@login_required
def billing_info_shops(request,id):
    context = {}
    context['object'] = Shops.objects.get(id=id)
    return render(request,'register/info_billing.html',context)

@login_required
def all_ctageor(request):
    context = {}
    context['objects_list'] = Cataegor.objects.all().order_by('-pk')
    return render(request,'register/categor.html',context)

class CreateCategorViews(CreateView):
    model = Cataegor
    form_class = CreateCatgeorForms
    template_name = 'register/crud_categor.html'
    success_url = reverse_lazy('all_ctageor')

class UpdateCategorViews(UpdateView):
    model = Cataegor
    form_class = CreateCatgeorForms
    template_name = 'register/crud_categor.html'
    success_url = reverse_lazy('all_ctageor')

class DeleteCategorViews(DeleteView):
    model = Cataegor
    template_name = 'register/delete_categor.html'
    success_url = reverse_lazy('all_ctageor')


@login_required
def notification_admin(request):
    context = {}
    context['objects_list'] = NotifikationsSendClient.objects.all().order_by('-id')
    return render(request,'register/all_noti.html',context)
@login_required
def deteile_notifi(request,id):
    objects = NotifikationsSendClient.objects.filter(id=id)
    return render(request,'register/deteile_noti.html',{'objects':objects})

@login_required
def verification(request,id):
    notification = NotifikationsSendClient.objects.filter(id=id)[0]
    notification.status_id = 3
    notification.save()
    return redirect('notification_admin')

@login_required
def rejection(request,id):
    notification = NotifikationsSendClient.objects.filter(id=id)[0]
    notification.status_id = 2
    balans = Balans.objects.get(shop_id=notification.shop_id)
    for item in NotificationStatus.objects.all():
            x = item.name
    summ = int(balans.amunt)+int(item.name)
    balans_confirm = Balans.objects.filter(shop_id=balans.shop_id).update(amunt=str(summ))
    notification.save()
    return redirect('notification_admin')

@login_required
def delete_notification(request,id):
    note = NotifikationsSendClient.objects.get(id=id)
    note.delete()
    return redirect('notification_admin')