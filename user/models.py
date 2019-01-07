from django.db import models


# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=30,verbose_name='用户名')
    email = models.EmailField(null=False,verbose_name='邮箱')
    pwd = models.CharField(max_length=100,verbose_name='密码')
    isActive = models.BooleanField(default=1,verbose_name='是否有效')

    def __str__(self):
        return self.name


    class Meta:
        #1.指定表名
        db_table = 'users'
        #2.指定在admin中显示的名称
        verbose_name='用户信息'
        #3.指定在admin中显示的名称
        verbose_name_plural=verbose_name




# '''地址模型管理器类'''
class AddressManager(models.Manager):
    '''地址模型管理器类'''
    # 1.改变原有查询的结果集:all()
    # 2.封装方法:用户操作模型类对应的数据表(增删改查)
    def get_default_address(self, user):
        '''获取用户默认收货地址'''
        # self.model:获取self对象所在的模型类
        try:
            address = self.get(user=user, is_default=True)  # models.Manager
        except self.model.DoesNotExist:
            # 不存在默认收货地址
            address = None

        return address



# 地址模型类
class Address(models.Model):
    user = models.ForeignKey('UserInfo', verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 自定义一个模型管理器对象
    objects = AddressManager()

    def __str__(self):
        return self.user.name

    class Meta:
        db_table = 'address'
        verbose_name = '用户收货地址'
        verbose_name_plural = verbose_name
