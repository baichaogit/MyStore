from django.conf.urls import url
from .views import *



#  user 应用的urls

urlpatterns = [
    url(r'^index/$',index_views,name='index'),
    url(r'^register/$',register_views,name='register'),
    url(r'^login/$',login_views,name='login'),
    url(r'^logout/$',logout_views,name='logout'),
    url(r'^personal/$',personal_views,name='personal'),
    url(r'^address/$',address_views,name='address'),
    url(r'^default_addr/$',default_addr_views,name='default_addr'),
    url(r'^update_addr/$',update_addr_views,name='update_addr'),
    url(r'^delete_addr/$',delete_addr_views,name='delete_addr'),
    url(r'verifycode/$',verifycode, name='verifycode'),
    url(r'^changecode/$',changecode_views, name='changeCode')
]