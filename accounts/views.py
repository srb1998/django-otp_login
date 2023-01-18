from django.shortcuts import render , redirect

from django.contrib.auth.models import User

from .models import Profile

import random

import http.client

from django.conf import settings
from dotenv import load_dotenv
import os

load_dotenv()


# Create your views here.


def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    message = otp
    authkey = os.getenv('AUTH_KEY')
    headers = { 'content-type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message=yourotpis"+message+"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    #Add in Url = +"&DLT_TE_ID="+
    conn.request("GET", url , headers=headers) 
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None



def login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        print(mobile)
        
        user = Profile.objects.filter(mobile = mobile).first()
        print(user)
        if user is None:
            context = {'message' : 'User not found' , 'class' : 'danger' }
            return render(request,'login.html' , context)
        
        otp = str(random.randint(1000 , 9999))
        print(otp)
        user.otp = otp
        user.save()
        send_otp(mobile , otp)
        request.session['mobile'] = mobile
        return redirect('otp')        
    return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        
        if check_user or check_profile:
            context = {'message' : 'User already exists' , 'class' : 'danger' }
            return render(request,'register.html' , context)
            
        user = User(username = email, first_name = name)
        user.save()
        otp = str(random.randint(1000 , 9999))
        print(otp)
        profile = Profile(user = user , mobile = mobile , otp = otp) 
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,'register.html')

def otp(request):
    mobile = request.session['mobile']
    context = {'mobile':mobile}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.filter(mobile = mobile).first()

        if otp == profile.otp:
            return redirect('cart')
        else:
            print("wrong otp")
            context = {'message' : 'Wrong OTP entered' , 'class' : 'danger' , 'mobile':mobile}
            return render(request,'otp.html',context)   
        
    return render(request,'otp.html' , context)