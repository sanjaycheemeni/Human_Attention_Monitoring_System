from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User
from  .models import UserData
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages


# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/session/')
    else:
        if request.method == 'POST':
            uname = request.POST.get('username')
            passw = request.POST.get('password')
            user = authenticate(request,username=uname,password=passw)
            if user is not None:
                login(request,user)
                return redirect('/session/')
            else:
                messages.error(request, 'Something wrong,Try again!')
        context={}
        return render(request,'login.html',context)







    # print(request.user)
    # if request.user.is_authenticated:
    #     print('###',request.user)
    #     return render(request,'dashboard.html')
    # if request.method == 'POST':
    #     uname = request.POST.get('username')
    #     passw = request.POST.get('password')
    #     user = authenticate(request,username=uname,password=passw)
    #     print(user)
    #     if user is not None :
    #         login(request,uname)
    #         return redirect('/main/')     
    #     else:
    #         messages.error(request, 'Something wrong,Try again!')  
    #         print('#wrong') 
    # else:
    #     print('hai')
    # return render(request,'login.html')



def userPage(request):
    return render(request,'session.html')


def indexPage(request):
    if request.method == 'POST':
        task=request.POST.get('task')
        print(task)
    return render(request,'test.html')
    # return render(request,'home.html')


def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect('/main/')
    else:
        if request.method == 'POST':
            uname = request.POST.get('uname')
            mail = request.POST.get('email')
            passw = request.POST.get('password')
            cpassw = request.POST.get('confirmpassword')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            # print(mail,uname,passw,age,gender)
            try:
                user = User.objects.create_user(username=uname,email=mail,password=passw)
                if user is not None:
                    data = UserData(user_name=uname,user_mail=mail,gender=gender,age=age,password=passw)
                    data.save()
                    print('Data stored to DDB')
                    return redirect('/login/')
                else:
                    print('error')
                    # messages.error(request, 'Something wrong,Try again!') 
            except:
                    messages.error(request, 'Can\'t create user,Check and try agian!') 

            # if user is not None:
            #     data = UserData(user_name=uname,user_mail=mail,gender=gender,age=age,password=passw)
            #     data.save()
            #     print('Data stored to DDB')
            #     return redirect('/login/')
            # else:
            #     print('error')
            #     messages.error(request, 'Something wrong,Try again!')  
            
        return render(request,'register.html'  )

@login_required(login_url='/login/')
def mainPage(request):
    return render(request,'session-member.html')

def contactUs(request):
    return render(request,'contact_us.html')



@login_required(login_url='/login/')  
def profilePage(request):
    current_user = request.user
    print(current_user.username)
    context = {'cur_usr':current_user}
    return render(request,'profile.html',context)

def logOutPage(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def curSession(request):
    # return render(request,'face_api/index.html')
    return render(request,'session-member.html')