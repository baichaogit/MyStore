import datetime
import time
from audioop import reverse

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
import logging

from good.models import GoodSKU
from user.models import Address
from .models import *

# Create your views here.



# 去 购物车页面
def cart_views(request):
    # 谁? 的购物车
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id)
        # 该用户已购买的商品
        sku_list = CartInfo.objects.filter(user=user)
        # 已购商品总数量
        total_count = 0
        for sku in sku_list:
            total_count += sku.ccount
        # 总价格
        total_price = 0
        for sku in sku_list:
            # 每种商品 小计 价格
            sku.amount = sku.good.price * int(sku.ccount)
            # 所有商品 总计价格
            total_price  += sku.amount
        # print('此人一共买了:', total_count, '件商品')
        # print('总价是:',total_price)

        return render(request, 'cart.html',locals())

    else:#没有登录
        return render(request, 'login.html', {"msg": "您还没有登录"})


# ----------------------

# ajax异步post请求
# 前端改变商品数量  后端也要进行数据库更新
def cart_update_views(request):
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')

    else:   # 未登录
        print('----update---用户没有登录')
        return JsonResponse({'res':'您还没有登录'})

    user = UserInfo.objects.filter(id=id)
    # 接收前端数据
    sku_id = request.POST.get('sku_id')  # 哪个商品的数量变了
    count = request.POST.get('count')    # 数量是多少
    print('++产品id+++',sku_id)
    if not all([sku_id, count]):
        print('----update---数据不完整')
        return HttpResponse({'res':'提交的数据不完整!'})

    try:
        sku = CartInfo.objects.get(user=user, good_id=sku_id)
        # print('--修改前----',sku.ccount)
        print('--要改成---',count)
        sku.ccount = int(count)
        sku.save()
        print('--修改后----', sku.ccount)
        return JsonResponse({'res':'ok'})

    except CartInfo.DoesNotExist:
        return JsonResponse({'res':'商品不存在'})




# --------------------

# ajax异步post请求
# 前端 删除 购物车商品  后端也要进行数据库更新
def cart_delete_views(request):
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
    else:  # 未登录
        print('----update---用户没有登录')
        return JsonResponse({'res': '您还没有登录'})

    user = UserInfo.objects.filter(id=id)
    # 获取前端数据
    # 接收前端数据
    sku_id = request.POST.get('sku_id')  # 要删除 哪一个商品
    try:
        sku = CartInfo.objects.get(user=user, good=sku_id)
        sku.delete()
        return JsonResponse({'res': 'ok'})
    except CartInfo.DoesNotExist:
        return JsonResponse({'res':'购物车不存在此商品'})





# -------------------------

# ajax (商品详情页, 用户点击购买按钮)

# 加购物车 操作
def add_cart_views(request):
    new_cart = CartInfo()

    # 谁? 点击了添加购物车
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id)

        # 添加的具体是什么商品
        sku_id = request.GET.get('sku_id')
        sku = GoodSKU.objects.filter(id = sku_id)

        if len(sku) > 0:
            new_cart.user = user[0]
            new_cart.good = sku[0]
        else:
            content = {'status': '2', 'text': '没有这个商品或没这个用户!'}
            jsonstr = json.dumps(content)
            return HttpResponse(jsonstr)
        try:
            oldgo = CartInfo.objects.filter(good_id=sku_id, user_id=id)
            print('-----',oldgo)
            if len(oldgo)>0:
                oldgo[0].ccount=oldgo[0].ccount + 1
                print('*******',oldgo[0].ccount)
                oldgo[0].save()
            else:
                new_cart.ccount = 1
                new_cart.save()

            content = {'status': '1', 'text': '购物车 添加成功'}
            jsonstr = json.dumps(content)
            return HttpResponse(jsonstr)

        except BaseException as e:
            logging.warning(e)
            content = {'status': '2', 'text': '添加失败!'}
            jsonstr = json.dumps(content)
            return HttpResponse(jsonstr)


    else:  # 用户没有登录
        content = {'status': '2', 'text': '您还没有登录'}
        jsonstr = json.dumps(content)
        return HttpResponse(jsonstr)











# 去 结算 页面 post
def jiesuan_views(request):

    # 谁? 在结算
    id = request.session.get('user_id')
    user = UserInfo.objects.filter(id=id)

    # 该用户的默认收货地址
    try:
        default_addr = Address.objects.get(user=user, is_default=True)
    except Address.DoesNotExist:
        default_addr = None

    # 接收前端数据  用户提交了哪几个 购物车
    cart_ids = request.POST.getlist('sku_ids')
    # print('-------cart_ids--------',cart_ids)

    # 检查一下参数
    if not cart_ids:
        # 跳转到购物车页面
        return redirect(reverse('order:cart'))  # 重定向到 购物车页面

    cart_list  = [ ] # 列表 存放 购物车对象
    cart_ids_list =[ ] # 列表 存放 购物车对象的id
    sku_count = 0  # 商品总件数
    total_price = 0 # 总金额
    for cart_id in cart_ids:
        cart = CartInfo.objects.filter(id=cart_id, user=user).first()
        cart.img = cart.good.goods.spu_img  # 购物车商品的图片
        cart.name = cart.good.goods.name # 名称
        cart.price = cart.good.price  # 单价
        cart.amount = cart.price * cart.ccount
        total_price += cart.amount
        sku_count += cart.ccount
        # print('小计-------',cart.amount)
        cart_list.append(cart)
        cart_ids_list.append(cart.id)
    # print('-----cart_ids_list------',cart_ids_list)
    return render(request, 'order_jiesuan.html',locals())





# ------提交 订单----------
def submit_order_views(request):
    # 谁? 在提交
    id = request.session.get('user_id')
    user = UserInfo.objects.filter(id=id).first()

    # 用户选择了 哪个地址
    addr_id = request.GET.get('addr_id')
    addr = Address.objects.filter(id = addr_id).first()

    # 订单时间 (订单号)
    orderTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    # 订单总价
    acounts = request.GET.get('acounts')
    # 订单总数
    acot = request.GET.get('acot')

    # 用户提交了哪几个 购物车(id)
    cart_ids_list_str = request.GET.getlist('cart_ids_list')[0]  # '[22, 23, 24]'  字符串
    list = cart_ids_list_str[1:-1].split(', ')
    print('-----///-------',list)
    acot = 0  # 商品总数
    acounts = 0 # 订单价格
    for cart_id in list:
        cart = CartInfo.objects.get(id=cart_id)
        try:
            Order.objects.create(user=user,cart=cart ,orderNo=orderTime,
                                 address=addr, acot=acot, acounts=acounts)
            print('-----提交-ok--------')
            return render(request, "index.html")
        except BaseException as e:
            logging.warning(e)
            print('-----提交失败-------',e)
            return render(request,"index.html")











# -------------------
# 所有订单
def all_order_views(request):


    return render(request,'order_all.html')





