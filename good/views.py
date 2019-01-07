
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
# Create your views here.



def single_views(request,good_id):
    # 所有 品牌实例
    brands = GoodBrand.objects.all()
    # 用户点击了哪个产品?
    good_id = good_id
    single_good = GoodSKU.objects.filter(id=good_id)

    # 和这个id的产品同类 但不同内存的 兄弟产品
    # other_goods = GoodSKU.objects.filter(goods=(single_good.goods.name))
    # print(other_goods)

    return render(request,'single.html',locals())




def products_views(request,brand_id):
    # 用户点击了哪个品牌?
    brand_id = brand_id
    # 所有 品牌实例
    brands = GoodBrand.objects.all()

    goods = GoodSKU.objects.filter(brand=brand_id)
    # print(goods)

    return render(request,'products.html',locals())

