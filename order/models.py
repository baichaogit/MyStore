# coding=utf-8

from django.db import models
from user.models import UserInfo, Address
from good.models import GoodSKU

ORDERSTATUS = (
    (1, "未支付",),
    (2, "已支付"),
    (3, "订单取消"),
)




class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    good = models.ForeignKey(GoodSKU, on_delete=models.CASCADE)
    ccount = models.IntegerField('数量', default=0)

    def __unicode__(self):
        return self.user

    # def __str__(self):
    #     return self.user.name

    def get_absolute_url(self):
        return '???'

    class Meta():
        db_table = 'cartinfo'




class Order(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartInfo,on_delete=models.CASCADE,default=None)
    orderNo = models.CharField("订单号", max_length=200)
    # ads = models.CharField("收件地址", max_length=200,default=None)
    address = models.ForeignKey(Address, null=True,default=None)
    acot = models.CharField("总数", max_length=200)
    acounts = models.CharField("价格", max_length=200)
    cals = models.TextField("orderdetail", null=True, blank=True,default=None)
    orderStatus = models.IntegerField("订单状态", blank=True, choices=ORDERSTATUS, default='1')

    def __unicode__(self):
        return self.user

    def get_orderStatusDisplay(self):
        if self.orderStatus == 1:
            return u'未支付'
        elif self.orderStatus == 2:
            return u'已支付'
        elif self.orderStatus == 3:
            return u'订单取消'
        else:
            return u''