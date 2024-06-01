from django.shortcuts import render

from django.http import HttpResponse
from app.forms import *

# Create your views here.

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
            return HttpResponse('Registration is Successsful')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'reg.html',d)