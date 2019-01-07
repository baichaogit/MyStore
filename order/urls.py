from django.conf.urls import url
from .views import *



#  order 应用的urls

urlpatterns = [
    url(r'^cart/$',cart_views,name='cart'),
    url(r'^pay/$',pay_views,name='pay')

]