from django.shortcuts import *
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from  .models import UserData,Session,sessionLog
from django.contrib.auth import logout,login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
import random
from django.http import JsonResponse
import time
from .models import session_members

#### 
def checkCurrentSession(id):
    as_host = Session.objects.values().filter(host_id=id)
    expired_sessions = []
    for row in as_host:
        # checks for already expired or not
        if int(row['end_time']) < current_milli_time():
            return row['session_key']
        else:
            expired_sessions.append(row['session_key'])
    as_member = session_members.objects.values().filter(user_id
    =id)
    for row in as_member:
        if id == row['user'] and row['session_key'] not in expired_sessions:
            return row['session_key']


def current_milli_time():
    return round(time.time() * 1000)



# check for session_key exist or not9999
def isExistingSession(ses_key):
    user_list = session_members.objects.values().filter(session_key=ses_key).filter(permission='ACTIVE')
    ses_list = Session.objects.values().filter(session_key=ses_key).filter(end_time='99999999')
    if ses_list.__len__()>0:
            return True
    return False

def isUSerHavePermission(key,usr_id,user):
    user_list = session_members.objects.values().filter(session_key=key).filter(user_id=usr_id)
    if user_list.__len__()>0:
        if user_list.filter(permission='ACTIVE'):
            return True
    else:
        data = session_members(session_key=key,user=user,user_id=usr_id,permission='INACTIVE')
        data.save()
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
    # key = request.POST.get('session_key')
    # session_list = Session.objects.values().filter(session_key=key).filter(end_time='888888')
    context={}
    if request.method =='POST':
        context={}
        ses_key = request.POST.get('session_key')
        if isExistingSession(ses_key):
            if isUSerHavePermission(ses_key,request.user.email,request.user.username):
                context = {'session_key' : ses_key}
                return render(request,'member-session.html',context)
        else:
            context={'err_msg':'Invalid session key or Session expired...!!'}
    return render(request,'session.html',context)

def home(request):
    isExistingSession('279275')
    val = 'Sign In'
    link ='/login'
    col = '#6C63FF'
    if request.user.is_authenticated:
        val = 'Log Out'
        link='/logout'
        col = '#ff1111'
    con = {'userStatus' :val,'link':link,'color':col}
    # checkCurrentSession(request.user.email)
    return render(request,'home.html',context=con)

def indexPage(request):
    # if request.method == 'POST':
    #     task=request.POST.get('task')
    #     print(task)
    print(request.is_ajax())
    if request.is_ajax() and request.method == 'POST':
        session_key =  request.POST.get('session_key')
        usr =  request.POST.get('user')
        mr =  request.POST.get('MR')
        ear =  request.POST.get('EAR')
        time_ms =current_milli_time()
        data = sessionLog(session_key=session_key,user=usr,mr=mr,ear=ear,time_ms=time_ms)
        data.save()
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
    # if 'first_time' in request.COOKIES:
    #     print(request.COOKIES['first_time'])
    # response = render(request,'test-ms.html',{})
    # response.set_cookie('first_time','yes',max_age=3600)
    # return response
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
    if request.is_ajax():
        print('testingggggg',request.POST.get('type'))
        data = 'done'
        key = str(request.COOKIES['session_key'])
        if request.POST.get('type') == 'accept':
            u = session_members.objects.get(session_key=key,user_id=request.POST.get('user'))
            u.permission = 'ACTIVE'
            u.save()
        if request.POST.get('type') == 'deny':
            u = session_members.objects.get(session_key=key,user_id=request.POST.get('user'))
            u.permission = 'INACTIVE'
            u.save()
        if request.POST.get('type') == 'None':
            data = list(session_members.objects.values().filter(session_key=key))#.filter(session_key=key))
        return JsonResponse({'data': data})
    
    session_key = random.randint(111111,999999)
    if 'in_a_session' in request.COOKIES:
        if request.COOKIES['in_a_session'] == 'TRUE':
            session_key = request.COOKIES['session_key']
    
    admin = request.user
    if not isExistingSession(session_key):
        data = Session(session_key=session_key,host_id=request.user.email,host_name=request.user.username,end_time="99999999")
        data.save()
    # print("Data ;",data)
    context = { 'session_key' : session_key,
                'session_admin':admin.username,
                'host_name':admin.email}
    response =  render(request,'host-session.html',context)
    if 'in_a_session' not in request.COOKIES:
        response.set_cookie('session_key',session_key,max_age=3600)
        response.set_cookie('in_a_session','TRUE',max_age=3600)
    return response






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
