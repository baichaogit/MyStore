import random

from django.db.models import Min
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pylint.reporters import json

from .models import *
# Create your views here.


# spu 单品详情页
def single_views(request,goods):
    # 所有 品牌实例
    brands = GoodBrand.objects.all()
    # 用户点击了哪个spu产品?
    goods = goods
    good_sku = GoodSKU.objects.filter(goods=goods)
    goods_name = good_sku[0].goods.name
    goods_detail = good_sku[0].goods.detail
    goods_img = good_sku[0].goods.spu_img
    for t in good_sku:
        print(t)


    return render(request,'single.html',locals())





# 品牌主页
def products_views(request,brand_id):
    # 用户点击了哪个品牌?
    brand_id = brand_id

    # 所有 品牌实例展示
    brands = GoodBrand.objects.all()

    # goods = GoodSKU.objects.filter(brand=brand_id)
    goods = GoodSKU.objects.filter(brand=brand_id).values('goods').annotate(minprice=Min('price')).\
            values('goods','goods__name','minprice','goods__spu_img')
    # for good in goods:
    #     print(good['goods__name'],good['minprice'])

    return render(request,'products.html',locals())

