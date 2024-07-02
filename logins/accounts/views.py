from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    flag=1
    obj=User.objects.all()
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
        pass2=request.POST.get('repassword')
        for i in obj:
            if uname==i.username:
                flag=0
        if pass1 !=pass2:
            messages.error(request,"please match the password")
            redirect('sign_up')
        elif len(pass1)<9:
            messages.error(request,"password has less than 8 characters")
            redirect('sign_up')

        elif flag==0:
            messages.error(request,"username already taken")
            redirect('sign_up')


        else:
            new_user=User.objects.create_user(uname,email,pass1)
            new_user.save()
            return redirect('login')

    return render(request,'sign_up.html')
@never_cache
def logins(request):
    if request.session.session_key:
        if request.user.is_staff:
            return redirect('admin')
        else:
            return redirect('home')
    if request.method=='POST':
        uname=request.POST.get('username')
        pass1=request.POST.get('password')
        User=authenticate(request,username=uname,password=pass1)
        if User:
            if User.is_staff:
                login(request,User)
                return redirect('admin')
            else:
                login(request,User)
                return redirect('home')
        else:
            messages.error(request,"invalid user")
            return redirect('login')

        

    return render(request,'login.html')
@never_cache
@login_required(login_url='login')
def home(request):
    if request.user.is_staff:
        return redirect('admin')
    
    user=request.user
    return render(request,'home.html',{'name':user})




@never_cache
@login_required(login_url='login')
def admin1(request):
    if request.method == 'POST':
        uname=request.POST.get('search')
        obj= User.objects.filter(username__icontains=uname,is_superuser=False)
        if obj:
            return render(request,'admin.html',{'obj':obj})
        else:
            messages.error(request,"invalid user")
            return render('admin')


        

    obj=User.objects.filter(is_superuser=False)
    dict={
        'obj':obj,
    }
    return render(request,'admin.html',dict)



def logouts(request):
    logout(request)
    return redirect('login')

@never_cache
def add(request):
    flag=1
    obj=User.objects.all()
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        for i in obj:
            if username==i.username:
                flag=0
        if flag==0:
            messages.error(request,"username already taken")


        else:
            new_user=User.objects.create_user(username,email,password)
            new_user.save()
            return redirect('admin')
@never_cache       
def edit(request):
    obj=User.objects.all()
    context={
        'obj':obj,
    }
    return redirect(request,'admin.html',context)
@never_cache
def update(request,id):
    if request.method == 'POST':
        unam=request.POST.get('username')
        email=request.POST.get('email')

        update_user=User(id=id,username=unam,email=email)
        update_user.save()
        return redirect('admin')
    return redirect(request,'admin.html')
@never_cache        
def delete1(request,id):
    User.objects.filter(id=id).delete()
    print(id)
    return redirect('admin')
