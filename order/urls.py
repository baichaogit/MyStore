from django.conf.urls import url
from .views import *



#  order 应用的urls

urlpatterns = [
    url(r'^cart/$',cart_views,name='cart'),
    url(r'^add_cart/$',add_cart_views,name='add_cart'),
    url(r'^update/$',cart_update_views,name='update',),
    url(r'^delete/$',cart_delete_views,name='delete',),
    url(r'^jiesuan/$',jiesuan_views,name='jiesuan'),
    url(r'^submit_order/$',submit_order_views,name='submit_order'),
    url(r'^all_order/$',all_order_views, name='all_order'),

]


