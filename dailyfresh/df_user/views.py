from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import *
from hashlib import sha1
# Create your views here.

def index(request):
    contxt = {'title': '天天生鲜-首页'}
    return render(request, 'df_user/index.html', contxt)

def register(request):
    contxt = {'title':'天天生鲜-注册'}
    return render(request,'df_user/register.html',contxt)

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    xieyi = post.get('allow')

    if upwd!=ucpwd:
        return redirect('/user/register/')

    if uname == '':
        return redirect('/user/register/')

    if upwd == '':
        return redirect('/user/register/')

    if uemail == '':
        return redirect('/user/register/')

    if xieyi != '1':
        return redirect('/user/register/')

    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd1 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd1
    user.uemail = uemail
    user.save()

    contxt = {'title': '天天生鲜-登录'}
    return render(request, 'df_user/login.html',contxt)

def login(request):
    uname = request.COOKIES.get('uname','')
    contxt = {'title': '天天生鲜-登录', 'error_name': '0',
              'error_pwd': '0', 'uname': uname}
    return render(request,'df_user/login.html',contxt)

def login_handle(request):
    contxt = {'title': '天天生鲜-用户中心'}
    
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu')

    users = UserInfo.objects.filter(uname=uname)

    if len(users)==1:
        s1 = sha1()
        s1.update(upwd.encode('utf8'))
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponseRedirect('/user/user_center_info/')
            if jizhu =='1':
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user.id'] = users[0].id
            request.session['user.name'] = uname
            return red
        else:
            contxt = {'title': '天天生鲜-登录','error_name':'0',
                      'error_pwd':'1','uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html/',contxt)
    else:
        contxt = {'title': '天天生鲜-登录', 'error_name': '1',
                  'error_pwd': '0', 'uname': uname, 'upwd': upwd}
        return render(request,'df_user/login.html/',contxt)

def user_center_info(request):
    user_email = UserInfo.objects.get(id=request.session['user.id']).uemail
    contxt = {'title': '天天生鲜-用户中心',
              'user_email':user_email,
              'user_name':request.session['user.name'],
              }
    return render(request,'df_user/user_center_info.html',contxt)

def user_center_order(request):
    contxt = {'title': '天天生鲜-用户中心'}
    return render(request,'df_user/user_center_order.html',contxt)

def user_center_site(request):
    user = UserInfo.objects.get(id=request.session['user.id'])

    if request.method == 'POST':
        post = request.POST
        user.urecipients = post.get('urecipients')
        user.uaddress = post.get('uaddress')
        user.upostcode = post.get('upostcode')
        user.uphone = post.get('uphone')
        user.save()

    contxt = {'title': '天天生鲜-用户中心','user':user}
    return render(request,'df_user/user_center_site.html',contxt)


