from django.conf.urls import url
from .views import *



#  order 应用的urls

urlpatterns = [
    url(r'^cart/$',cart_views,name='cart'),
    url(r'^order/$',order_views,name='order'),
    url(r'^add_cart/$',add_cart_views,name='add_cart'),
    url(r'^update/$',cart_update_views,name='update',),
]


