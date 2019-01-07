from django.contrib import admin
# Register your models here.
from .models import *



class BrandAdmin(admin.ModelAdmin):
    list_display = ['name','logo','image']
    list_display_links = ['logo']
    list_editable = ['name']
    # 添加允许被搜索的字段们
    search_fields = ['name']
    # 指定每条数据的 详情页 中显示的字段及排列的顺序
    fileds = ['name']




class SKUAdmin(admin.ModelAdmin):
    list_display = ['goods','name','price','neicun','stock','sales']
    list_editable = [ 'name', 'price', 'stock']
    # 添加允许被搜索的字段们
    search_fields = ['brand','name']
    # 指定每条数据的 详情页 中显示的字段及排列的顺序
    fileds = ['name']




class SPUAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'detail','spu_img']
    list_editable = ['detail','spu_img']
    search_fields = ['name']
    fileds = ['name']




class GoodImageAdmin(admin.ModelAdmin):
    list_display = ['sku' ]



class AddAdmin(admin.ModelAdmin):
    list_display = ['title']



class Add3Admin(admin.ModelAdmin):
    list_display = ['title','word']





admin.site.register(GoodBrand, BrandAdmin)

admin.site.register(GoodSKU, SKUAdmin)

admin.site.register(Goods, SPUAdmin)

admin.site.register(GoodImage, GoodImageAdmin)

admin.site.register(IndexAdd, AddAdmin)

admin.site.register(IndexAdd3, Add3Admin)

admin.site.register(Dingwei)




















