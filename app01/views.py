from utils.page import userList
from utils.response import BaseResponse

import json,time
from db import models
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.request import QueryDict
#Create your views here.

from io import BytesIO
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    # # img, code = create_validate_code()
    # img.save(stream, 'PNG')
    # request.session['CheckCode'] = code
    # return HttpResponse(stream.getvalue())

def auth_login(func):
    """
    判断用户是否登录的装饰器
    :param func:
    :return:
    """
    def inner(request, *args, **kwargs):
        try:
            username = request.session['username']
            return func(request, *args, **kwargs)
        except Exception as e:
        # except KeyError as e:
            print(repr(e))
            print("当前尚未登录")
            return redirect(reverse('web:login'))
    return inner

def user_verify(username, password):
    user_info = models.UserInfo.objects.filter(name=username, password=password).first()
    if not user_info:
        return False
    return user_info


class Login(View):
    def get(self,request,*args,**kwargs):
        # for user in range(50):
        #     models.UserInfo.objects.create(name='user{}'.format(user),password='123', email='{}'.format('user'+str(user)+'@qq.com'))
        return render(request,'login.html')

    def post(self,request,*args,**kwargs):
        name = request.POST.get('user',None)
        password = request.POST.get('password',None)
        # print(name,password,'----------------------------')
        user_info = user_verify(name, password)
        if user_info:
            # print(type(user_info), user_info.age)
            request.session['username'] = name
            # request.session.set_expiry(600)
        else:
            print("用户名或密码错误")
            return redirect(reverse('web:login'))

        return redirect(reverse('web:user_info'))


class LogOut(View):
    def get(self,request,*args,**kwargs):
        if request.session.get('username', None):
            del request.session['username']
        request.session.clear_expired()
        return redirect(reverse('web:login'))


@method_decorator(auth_login, name="dispatch")
class UserInfo(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'userinfo.html')


@method_decorator(auth_login, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class UserJson(View):
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            u_id = request.GET.get('key[id]', None)
            print(request.GET)
            if u_id:
                data_list = models.UserInfo.objects.filter(id=u_id).values()
                data_list = list(data_list)
                response.count = len(data_list)
                response.data = data_list
            else:
                data_list = list(models.UserInfo.objects.all().values())
                data_dict = userList(request, data_list)
                response.__dict__.update(data_dict)
        except Exception as e:
            response.code = 1000
            response.msg = str(e)
        print(response.__dict__)
        return HttpResponse(json.dumps(response.__dict__))

    def put(self, request, *args, **kwargs):
        """通过 用户-id 修改用户账号"""
        response = BaseResponse()
        response.code = 1000
        response.msg = "待开发"
        return HttpResponse(json.dumps(response.__dict__))

    def delete(self, request, *args, **kwargs):
        """通过 用户-id 删除用户账号"""
        response = BaseResponse()
        uid = QueryDict(request.body, encoding='utf-8').getlist('uid')[0]
        print(uid, type(uid))
        models.UserInfo.objects.filter(id=uid).delete()
        return HttpResponse(json.dumps(response.__dict__))


@method_decorator(auth_login, name="dispatch")
class AddUser(View):
    """创建用户登录账号"""
    def get(self, request, *args, **kwargs):
        return render(request, 'create_user.html')

    def post(self, request, *args, **kwargs):
        try:
            email = request.POST.get('email',None)
            if models.UserInfo.objects.filter(email=email).first():
                return HttpResponse("alert('添加失败,用户已存在')")

            models.UserInfo.objects.create(
                name=request.POST.get('user'),
                password=request.POST.get('password'),
                email=request.POST.get('email'),
            )
        except Exception as e:
            return HttpResponse("alert('创建失败,{}')".format(str(e)))

        return redirect(reverse('web:user_info'))


@method_decorator(auth_login, name="dispatch")
class ProjectManage(View):
    def get(self, request, *args, **kwargs):
        """项目列表页"""
        return render(request, 'project_manage.html')


@method_decorator(auth_login, name="dispatch")
class ProjectJson(View):
    def get(self, request, *args, **kwargs):
        """加载项目列表数据"""
        response = BaseResponse()
        try:
            a_id = request.GET.get('key[id]', None)
            print(request.GET)
            if a_id:
                data_list = list(models.Business.objects.filter(id=a_id).values())
                response.count = len(data_list)
                response.data = data_list
            else:
                data_list = list(models.Business.objects.all().values())
                data_dict = userList(request, data_list)
                response.__dict__.update(data_dict)
        except Exception as e:
            response.code = 1000
            response.msg = str(e)
        print(response.__dict__)
        return HttpResponse(json.dumps(response.__dict__))

    def put(self, request, *args, **kwargs):
        """通过 项目-id 修改项目信息"""
        pass

    def delete(self, request, *args, **kwargs):
        """通过 项目-id 删除项目"""
        pass


@method_decorator(auth_login, name="dispatch")
class AddProject(View):
    """添加新 项目/业务线"""
    def get(self, request, *args, **kwargs):
        return render(request,'create_app.html')

    def post(self, request, *args, **kwargs):
        try:
            app_name = request.POST.get('name',None)
            if models.UserInfo.objects.filter(email=app_name).first():
                return HttpResponse("alert('添加失败,应用已存在')")

            models.Business.objects.create(
                name=request.POST.get('name'),
                command=request.POST.get('cmd'),
            )
        except Exception as e:
            return HttpResponse("alert('创建失败,{}')".format(str(e)))

        return redirect(reverse('web:app_manage'))


@method_decorator(auth_login, name="dispatch")
class ReleaseProject(View):
    """发布项目"""
    def get(self, request, *args, **kwargs):
        response = BaseResponse()
        try:
            aid = request.GET.get('aid')
            cmd = models.Business.objects.filter(id=aid).values('command').first()
            # print(cmd, cmd['command'])
            cmd = cmd['command'].split()
            print(cmd)
            import subprocess
            # res = subprocess.check_call(cmd)
            time.sleep(3)
            res = 0
            if res:
                response.code = 1001

        except Exception as e:
            response.code = 1001
            response.error = str(e)

        return HttpResponse(json.dumps(response.__dict__))

    def post(self, request, *args, **kwargs):
        pass