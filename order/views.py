import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
import logging

from good.models import GoodSKU
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





















# 去 订单 页面
def order_views(request):

    return render(request, 'place_order.html')




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









