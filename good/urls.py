from django.conf.urls import url
from .views import *







#  good 应用的urls

urlpatterns = [
    url(r'^single/(?P<goods>\d+)$', single_views, name='single'),
    url(r'^products/(?P<brand_id>\d+)$',products_views,name='prodocts'),
]