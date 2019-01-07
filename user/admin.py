from django.contrib import admin

# Register your models here.

from .models import *



class UsersAdmin(admin.ModelAdmin):
    list_display = ['name','pwd','email','isActive']
    list_display_links = ['name','email']
    list_editable = ['isActive']
    # 4.添加允许被搜索的字段们
    search_fields = ['name']
    # 5.右侧增加过滤器
    list_filter = ['name','isActive']
    # 7.指定每条数据的 详情页 中显示的字段及排列的顺序
    fileds = ['name']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','receiver','addr','is_default']





admin.site.register(UserInfo, UsersAdmin)
admin.site.register(Address, AddressAdmin)
