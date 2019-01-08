import random
import re
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min
from django.shortcuts import render
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse

from good.models import IndexAdd, IndexAdd3, GoodSKU, Dingwei, GoodBrand
from .models import *
from django.contrib.auth.hashers import make_password,check_password

auth_check = 'renyidezifuchuan'  # 加密密钥

# index主应用 视图函数





# 进入主页
def index_views(request):
    # 主页最大号广告图
    add1 = IndexAdd.objects.all()[0]

    # 主页三幅中号广告
    add3 = IndexAdd3.objects.all()[0]

    # 所有 品牌
    brands = GoodBrand.objects.all()

    # t = GoodSKU.objects.filter(dingwei__goodsku=3)
    # print('-----',t)

    # 随机推荐(高端机) 4台
    goods_gao = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price')).values('goods','goods__name','minprice','goods__spu_img').filter(minprice__gt=5000)),4)

    # 随机推荐 (中端机) 4台
    goods_zhong = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price')).values('goods','goods__name','minprice','goods__spu_img').filter(minprice__range=[3000,4999])),4)

    # 随机推荐(低端机) 4台
    goods_di = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price')).values('goods', 'goods__name', 'minprice','goods__spu_img').filter(minprice__lt=3000)), 1)


    # 从request.session中获取登陆信息 判断用户是否登录????
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id).first()
        context = {
            'user': user,
            'brands':brands,
            'add1': add1,
            'add3': add3,
            # 'dingwei':dingwei,
            'goods_gao':goods_gao,
            'goods_zhong':goods_zhong,
            'goods_di':goods_di,
        }

# 如果用户没有登录
    context = {
        'brands': brands,
        'add1': add1,
        'add3': add3,
        # 'dingwei':dingwei,
        'goods_gao': goods_gao,
        'goods_zhong': goods_zhong,
        'goods_di': goods_di,

    }

    return render(request,'index.html',locals())









# 个人中心
def personal_views(request):
    # 从request.session中获取登陆信息 判断用户是否登录????
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id).first()

        return render(request,'user_center_info.html')
    else:
        return render(request, 'login.html', {"msg": "请登陆后 再进入用户中心"})





# 用户注册
def register_views(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        uemail = request.POST.get('uemail')
        upwd = request.POST.get('upwd')
        upwd2 = request.POST.get('upwd2')

        if not all([uname,uemail,upwd,upwd2]):
            return render(request,'register.html',{'msg':'您刚才提交的数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', uemail):
            return render(request, 'register.html', {'msg': '您刚才输入的邮箱格式不正确'})

        try:
            res = UserInfo.objects.filter(name=uname)
            if res:
                return render(request, 'register.html', {'msg': '您刚才输入的用户名已存在'})
        except ObjectDoesNotExist as e:
            logging.warning(e)

        if upwd != upwd2:
            return render(request, 'register.html', {'msg': '您刚才输入的两次密码不一致'})

        # 数据完全ok, 则进存数据库
        # 先把密码加密
        pwd_s = make_password(upwd,auth_check,'pbkdf2_sha1')
        new_user = UserInfo()
        new_user.name = uname
        new_user.email = uemail
        new_user.pwd = pwd_s
        new_user.save()
        return render(request,'login.html')






# 登陆
def login_views(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        uname = request.POST.get('uname')
        upwd = request.POST.get('upwd')
        if not all([uname,upwd]):
            return render(request, 'login.html', {"msg": "用户名和密码不能为空"})

        else:
            pwd_s = make_password(upwd, auth_check, 'pbkdf2_sha1')
            try:
                res = UserInfo.objects.filter(name=uname, pwd=pwd_s)
                if res:
                    # 把登陆信息存到 session
                    request.session['user_id'] = res[0].id
                    request.session['user_name'] = uname
                    print('-------------保存session成功------------')
                    # 登陆成功-------  重定向到 主页
                    return redirect('/user/index')
            except ObjectDoesNotExist as e:
                logging.warning(e)
            return render(request, 'login.html', {"msg": "用户名或密码错误"})





# 退出
def logout_views(request):
    try:
        if request.session['user_name']:
            del request.session['user_id']
            del request.session['user_name']
    except KeyError as e:
        logging.warning(e)
    return redirect('/user/index')



