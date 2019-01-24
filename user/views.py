import random
import re
from audioop import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min
from django.shortcuts import render
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from good.models import IndexAdd, IndexAdd3, GoodSKU, Dingwei, GoodBrand
from order.models import CartInfo
from .models import *
from django.contrib.auth.hashers import make_password,check_password

auth_check = 'renyidezifuchuan'  # 加密密钥

# index主应用 视图函数




# 进入主页
def index_views(request):

    # 顶部最大号广告图
    add1 = random.sample(list(IndexAdd.objects.all()),1)[0]

    # 主页三幅中号广告
    add3_list = IndexAdd3.objects.all()

    # 所有 品牌
    brands = GoodBrand.objects.all()

    # 随机推荐(高端机) 4台
    goods_gao = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price'))
                .values('goods','goods__name','minprice','goods__spu_img','goods__screen','goods__cpu','goods__point')
                .filter(minprice__gt=5000)),4)

    # 随机推荐 (中端机) 4台
    goods_zhong = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price'))
                .values('goods','goods__name', 'minprice', 'goods__spu_img', 'goods__screen','goods__cpu', 'goods__point')
                .filter(minprice__range=[3000,4999])),4)

    # 随机推荐(低端机) 4台
    goods_di = random.sample(list(GoodSKU.objects.values('goods').annotate(minprice=Min('price'))
            .values('goods', 'goods__name', 'minprice', 'goods__spu_img', 'goods__screen','goods__cpu', 'goods__point')
            .filter(minprice__lt=3000)), 4)


    # 从request.session中获取登陆信息 判断用户是否登录????
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id).first()
        if user:
            # 该用户 已购商品
            sku_list = CartInfo.objects.filter(user=user)
            print('+++++',sku_list)
            # 已购商品总数量
            total_count = 0
            for sku in sku_list:
                total_count += sku.ccount
            print('此人一共买了:',total_count,'件商品')

            context = {
                'user': user,
                'brands':brands,
                'add1': add1,
                'add3': add3_list,
                # 'dingwei':dingwei,
                'goods_gao':goods_gao,
                'goods_zhong':goods_zhong,
                'goods_di':goods_di,
                'total_count':total_count,
        }

# 如果用户没有登录
    context = {
        'brands': brands,
        'add1': add1,
        'add3': add3_list,
        # 'dingwei':dingwei,
        'goods_gao': goods_gao,
        'goods_zhong': goods_zhong,
        'goods_di': goods_di,
        'total_count': 0,

    }

    return render(request,'index.html',locals())









# 个人中心

def personal_views(request):
    # 从request.session中获取登陆信息 判断用户是否登录????
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id).first()
        return render(request,'user_center_info.html',locals())

    else:
        return render(request, 'login.html', {"msg": "请登陆后 再进入用户中心"})



# 管理地址 页
def address_views(request):
    if request.method == 'GET':
        # 从request.session中获取登陆信息 判断用户是否登录????
        if 'user_id' in request.session and 'user_name' in request.session:
            id = request.session.get('user_id')
            user = UserInfo.objects.filter(id=id).first()
            address_list = Address.objects.filter(user=user)
            address_list = list(address_list) # 列表化
            for addr in address_list:
                if addr.is_default:
                    default_addr = addr # 找到了默认地址
                    address_list.remove(addr)

            return render(request,'user_address.html',locals())

        else:
            return render(request,'login.html',{"msg": "请登陆后 再进入用户中心"})


    # 添加 新地址
    if request.method == 'POST':
        print('++++++用户在添加地址++++++++++')
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id).first()
        # # 接收数据
        receiver = request.POST.get('receiver')  # 收件人
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver, addr, zip_code, phone]):
            print('*****数据不完整***********')
            return render(request, 'user_address.html', {'res': '添加失败, 数据不完整'})

        # 校验手机号
        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_address.html', {'res':'手机格式不正确'})
        # 拿到 默认地址
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            # 不存在默认收货地址
            address = None
        if address:
            is_default = False
        else:
            is_default = True
        # 添加 新地址
        Address.objects.create(user=user, receiver=receiver,
                               addr=addr, zip_code=zip_code,
                               phone=phone, is_default=is_default)
        return redirect('/user/address')  # 重定向回去






# 更改 默认地址
def default_addr_views(request):
    # 谁在改默认地址
    user_id = request.session.get('user_id')
    user = UserInfo.objects.filter(id = user_id)[0]
    # 接收前端的数据   用户要改哪一个地址
    new_default_id = request.GET.get('id')
    # 找到以前的 默认地址
    try:
        old_addr = Address.objects.get(user=user, is_default=True)
        old_addr.is_default = False
        old_addr.save()
    except Address.DoesNotExist:
        # 不存在默认收货地址
        old_addr = None
        return render(request, 'user_address.html', {'res': '操作失败'})


    new_addr = Address.objects.get(user=user, id=new_default_id)
    new_addr.is_default = True
    new_addr.save()
    return redirect('/user/address')  # 重定向回去






# 删除 地址
def delete_addr_views(request):
    # 谁在删除地址
    user_id = request.session.get('user_id')
    user = UserInfo.objects.filter(id = user_id)[0]
    # 接收前端的数据   用户要删哪一个地址
    delete_id = request.GET.get('id')
    # 找到这个地址
    try:
        delete_addr = Address.objects.get(user=user, id=delete_id).delete()
        return redirect('/user/address')  # 重定向回去
    except Address.DoesNotExist:
        # 不存在默认收货地址
        old_addr = None
        return render(request, 'user_address.html', {'res': '操作失败'})


# 修改 地址
def update_addr_views(request):
    # 谁在删除地址
    user_id = request.session.get('user_id')
    user = UserInfo.objects.filter(id = user_id)[0]
    # 接收前端的数据   用户要删哪一个地址
    update_id = request.GET.get('id')
    # 找到这个地址
    try:
        update_addr = Address.objects.get(user=user, id=update_id).delete()
        return redirect('/user/address')  # 重定向回去
    except Address.DoesNotExist:
        # 不存在默认收货地址
        old_addr = None
        return render(request, 'user_address.html', {'res': '操作失败'})


























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
        response = render(request, 'login.html')
        # 把源路径 存进cookie
        origin_url = request.META.get('HTTP_REFERER', '/')
        response.set_cookie('origin_url', origin_url, 60*60)
        return response


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
                    # 登陆验证成功-------  重定向到 源网页!!
                    # 取出 源路径
                    origin_url = request.COOKIES['origin_url']
                    # print('////////////',origin_url)
                    return redirect(origin_url)
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





# -----------------------------------------

# 生成验证码
from PIL import Image, ImageDraw, ImageFont

def rmdRGB():
    C1 = random.randrange(0,255)
    C2 = random.randrange(10,255)
    C3 =random.randrange(60,255)
    return (C1,C2,C3)

def verifycode(request):
    # 背景色，长度，宽度
    # bgcolor = '#997679'
    bgcolor = '#FFFFFF'
    width = 100
    height = 30
    # 创建画布
    im = Image.new('RGB',(width,height),bgcolor)
    # 创建画笔
    draw = ImageDraw.Draw(im)
    # 画点
    for i in range(0, 100):
        xy=(random.randrange(0,width),random.randrange(0,height))
        fill=(random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill=fill)

    # 添加文字
    str1 = 'ABCD123DEFGHIJK456LMNOPQRS789TUVWXYZ0'
    rand_str = ''
    for i in range(0,4):
        rand_str += str1[random.randrange(0,len(str1))]
    font = ImageFont.truetype('C:\Windows\Fonts\seguibl.ttf',23)
    draw.text((5,2),rand_str,fill=rmdRGB(),font=font)


    # 添加干扰线
    for i in range(3):
        x1 = random.randrange(0,width)
        y1 = random.randrange(0,height)
        x2 = random.randrange(0,width)
        y2 = random.randrange(0, height)
        draw.line((x1,y1,x2,y2),fill=rmdRGB())

    # 添加圆
    for i in range(20):
        x = random.randrange(0, width)
        y = random.randrange(0, height)
        draw.arc((x,y,x+4,y+4),0,90,fill=rmdRGB())

    # 结束
    del draw
    import io
    buf = io.BytesIO()
    im.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')




# 局部 刷新  二维码
def changecode_views(request):
    res = verifycode(request)
    # print('--------',res)
    dict = {
        1:'11111111'
    }

    return json.dumps(dict)



