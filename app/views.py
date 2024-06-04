from django.shortcuts import render

from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *

from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse 

from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    EUFO=UserForm()
    EPFO=ProfileForm()
    d={'EUFO':EUFO,'EPFO':EPFO}
    
    if request.method == 'POST' and request.FILES :
        NMUFDO = UserForm(request.POST)
        NMPFDO = ProfileForm(request.POST,request.FILES)
        
        if NMUFDO.is_valid() and NMPFDO.is_valid():
            MUFDO = NMUFDO.save(commit=False) #by using commit=false the data will not store into DB.
            PW = NMUFDO.cleaned_data['password']
            MUFDO.set_password(PW) #to encrpyt the data we use set_password.
            MUFDO.save()
            
            MPFDO = NMPFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()
            
            send_mail('Registration',
                      'Thank you for Registration.',
                      'peerushaik313@gmail.com',
                      [MUFDO.email],
                      fail_silently=False,)
            
            return HttpResponse('Registration is Successsful')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'reg.html',d)

def user_login(request):
    if request.method == 'POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Your Not a Authenticate User.')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
