from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User
from  .models import UserData,Session
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
import random
from django.http import JsonResponse

#### 
# check for session_key exist or not9999
def isExistingSession(ses_key):
    if ses_key == '123456':
        return True
    return False


###

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
    context={}
    if request.method =='POST':
        context={}
        ses_key = request.POST.get('session_key')
        if isExistingSession(ses_key):
            context = {'session_key' : ses_key}
            return render(request,'member-session.html',context)
        else:
            context={'err_msg':'Invalid session key or Session expired...!!'}
    return render(request,'session.html',context)


def indexPage(request):
    # if request.method == 'POST':
    #     task=request.POST.get('task')
    #     print(task)
    print(request.is_ajax())
    if request.is_ajax() and request.method == 'POST':
        print(request.POST)
        return JsonResponse({
            'msg' : 'true'
        })
    return render(request,'member-session.html',{'session_key' : '123456','user':'testuser'})
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
                    print('Data stored to DDB',data)
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



# new session creation
@login_required(login_url='/login/')
def newSession(request):
    session_key = random.randint(111111,999999)
    admin = request.user
    data = Session(session_key=session_key,host_id=request.user.email,host_name=request.user.username,end_time="99999999")
    data.save()
    # print("Data ;",data)
    context = { 'session_key' : session_key,
                'session_admin':admin.username,
                'host_name':admin.email}
    return render(request,'host-session.html',context)




## testingggggggggggggggggggg....


def test(r):
    print(r.is_ajax())
    if r.is_ajax():
        print(r.POST.get('name'))
        return JsonResponse({
            'msg' : 'true'
        })
    # if r.method == 'POST':
    #     print(r.POST.get('name'))
    return render(r,'test-ajax.html')
