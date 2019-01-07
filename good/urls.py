from django.conf.urls import url
from .views import *







#  user 应用的urls

urlpatterns = [
    url(r'^single/(?P<good_id>\d+)$', single_views, name='single'),
    url(r'^products/(?P<brand_id>\d+)$',products_views,name='prodocts'),
]