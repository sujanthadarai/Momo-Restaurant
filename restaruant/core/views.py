from django.shortcuts import render,redirect
from .models import Category,Momo,Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

import logging

logger=logging.getLogger('django')

# Create your views here.
# @login_required(login_url='log_in')
def index(request):
    cate=None
    momo=None
    
    try:
        cateid=request.GET.get('category')
    
        if cateid:
            momo=Momo.objects.filter(category=cateid)
        else:
            momo=Momo.objects.all()
        
        cate=Category.objects.all()
        
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            message=request.POST['message']
            Contact.objects.create(name=name,email=email,message=message,phone=phone)
            return redirect('index')
    
    except Exception as e:
        logger.error(str(e),exc_info=True)
    
    
 
    context={
        'cate':cate,
        'momo':momo,
        'date':datetime.now()
    }
    return render(request,'core/index.html',context)

@login_required(login_url='log_in')
def about(request):
    return render(request,'core/about.html')

@login_required(login_url='log_in')
def menu(request):
    return render(request,'core/menu.html')


'''
=====================================================================================
=====================================================================================
                             Authentication Part
=====================================================================================
=====================================================================================
'''
def register(request):
    if request.method == 'POST':
        fname=request.POST['first_name'] #sujan
        lname=request.POST['last_name'] #thadarai
        username=request.POST['username'] #sujan710
        email=request.POST['email'] #sujan@gmail.com
        password=request.POST['password']#ram
        password1=request.POST['password1'] #ram
        
        if password == password1:
            
            error=[] #["username  already register!!!","your password must contain at least one upper case"]
            if User.objects.filter(username=username).exists():
                error.append('username  already register!!!')
                
            
            if User.objects.filter(email=email).exists():
                error.append('email  already register!!!')
                
            
            if not re.search(r'[A-Z]',password):
                error.append('your password must contain at least one upper case')
               
            if not re.search(r'\d',password):
                error.append('your password must contain at least one digit')
                
            if  not error:

                try:
                    validate_password(password)
                    User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                    messages.success(request,"your account is successfully register!!!")
                    return redirect('register')
                except ValidationError as e:
                    for i in e.messages:
                        messages.error(request,i)
                    return redirect('register')
            else:
                for i in error:
                    messages.error(request,i)
                return redirect('register')

        else:
            messages.error(request,'Your password and confirm password doesnot match')
            return redirect('register')
            
    return render(request,'accounts/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST.get('username') #sujan1
        password=request.POST.get('password') #ram
        remember_me=request.POST.get('remember_me') #on or None
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet")
            return redirect('log_in')
        
        user=authenticate(username=username,password=password) #hari2 if not -->None
        
        if user is not None:
            login(request,user)
            
            if remember_me:
                request.session.set_expiry(120000000)
            else:
                request.session.set_expiry(0)
            
            next=request.POST.get('next','') #/menu/
            
            return redirect(next if next else "index")
        else:
            messages.error(request,'password doesnot match')
            return redirect('log_in')
    next=request.GET.get('next','') #/menu/
            
    return render(request,'accounts/login.html',{'next':next})



def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def password_change(request):
    
    form=PasswordChangeForm(user=request.user)
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        
    return render(request,'accounts/password_change.html',{'form':form})


# pip freeze > requirements.txt 

# pip install -r requirements.txt



#Domain name :www.facebook.com

# https://www.facebook.com
# https -->protocol
# www. -->sub domain
# facebook -->domain name 
# .com -->top level domain

#hosting  :service of storing

#shared hosting : 
#vps :
#dedicated hosting :
#cloud hosting :
