import random

from django.db.models import Min
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pylint.reporters import json

from order.models import CartInfo
from user.models import UserInfo
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# spu 单品详情页
def single_views(request,goods):
    # 从request.session中获取登陆信息 判断用户是否登录????
    if 'user_id' in request.session and 'user_name' in request.session:
        id = request.session.get('user_id')
        user = UserInfo.objects.filter(id=id)[0]


        if user:
            # 该用户 已购商品
            sku_list = CartInfo.objects.filter(user=user)
            print('+++++',sku_list)
            # 已购商品总数量
            total_count = 0
            for sku in sku_list:
                total_count += sku.ccount
            print('此人一共买了:',total_count,'件商品')


    # 所有 品牌实例
    brands = GoodBrand.objects.all()

    # 顶部最大号广告图
    add1 = random.sample(list(IndexAdd.objects.all()),1)[0]

    # 用户点击了哪个spu产品?
    goods = goods



    # 把用户点击的产品的id 存进cookies(浏览记录)
    pass

    good_sku = GoodSKU.objects.filter(goods=goods).order_by('price')
    goods_name = good_sku[0].goods.name
    goods_detail = good_sku[0].goods.detail
    goods_img = good_sku[0].goods.spu_img
    return render(request, 'single.html', locals())






# -------------------------------

# 品牌主页
def products_views(request,brand_id):
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

    # 用户点击了哪个品牌?
    brand_id = brand_id

    # 顶部最大号广告图
    add1 = random.sample(list(IndexAdd.objects.all()),1)[0]

    # 所有 品牌实例展示
    brands = GoodBrand.objects.all()


    goods_all = GoodSKU.objects.filter(brand=brand_id).values('goods').annotate(minprice=Min('price'))\
        .values('goods', 'goods__name', 'minprice', 'goods__spu_img', 'goods__screen', 'goods__cpu', 'goods__point')

    brand_name = GoodBrand.objects.filter(id=brand_id)[0]         # 品牌名
    brand_image = GoodBrand.objects.filter(id=brand_id)[0].image  # 品牌图片

    # # ------------ 分页显示 -----------
    paginator = Paginator(goods_all, 4, allow_empty_first_page=True)  # 分页对象 (每一页显示4个商品对象)
    page = request.GET.get('page')  # 得到 前端点击了哪个页码
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)

    return render(request,'products.html',locals())

