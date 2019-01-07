from django.db import models
from tinymce.models import HTMLField


# Create your models here.


# 品 牌
class GoodBrand(models.Model):
    name = models.CharField(max_length=30,verbose_name='品牌名')
    logo = models.CharField(null=True, max_length=20, verbose_name='商标')
    image = models.ImageField(null=True, upload_to='static/brand_img', verbose_name='商标图片')

    def __str__(self):
        return self.name

    class Meta:
        #1.指定表名
        db_table = 'good_brand'
        #2.指定在admin中显示的名称
        verbose_name='产品品牌'
        #3.指定在admin中显示的名称
        verbose_name_plural=verbose_name




# 商品SKU 模型
class GoodSKU(models.Model):
    neicun_choices=(
        (0,'4+32G'),(1,'4+64G'),
        (2,'6+64G'),(3,'6+128G'),(4,'6+256G'),
        (5,'8+64G'), (6,'8+128G'),(7,'8+256G'),
        (8, '64G'), (9,'128G'), (10,'256G'),(11,'512G'),(12,'32G')
    )
    status_choices = ((0,'下线'), (1,'上线'),)
    brand =  models.ForeignKey('GoodBrand', verbose_name='产品品牌')
    goods = models.ForeignKey('Goods',verbose_name='产品SPU')
    dingwei = models.ForeignKey('Dingwei',verbose_name='价格定位')
    name = models.CharField(max_length=20, verbose_name='产品名称')
    desc = models.CharField(max_length=256, verbose_name='产品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    neicun = models.SmallIntegerField(default=1, choices=neicun_choices, verbose_name='内存')
    image = models.ImageField(upload_to='static/sku_img', default='null',verbose_name='产品图片')
    stock = models.IntegerField(default=1, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='产品状态')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'good_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name





# 商品 SPU 模型
class Goods(models.Model):
    name = models.CharField(max_length=20, verbose_name='产品SPU名')
    # 富文本类型:带有格式的文本
    detail = HTMLField(blank=True, verbose_name="产品详情")
    spu_img = models.ImageField(upload_to='static/spu_img', default='null',verbose_name='产品图片')
    # 有了一个隐式属性 goodsku_set

    def __str__(self):
        return self.name

    class Meta:
        db_table = "good_spu"
        verbose_name = "商品SPU"
        verbose_name_plural=verbose_name




# # 首页 高/中/低端分类
class Dingwei(models.Model):
    dingwei_choices=((0,'高端旗舰'),(1,'中端爆款'),(2,'实用畅销'),)
    name = models.SmallIntegerField(default=1, choices=dingwei_choices, verbose_name='产品定位')

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "good_dingwei"
        verbose_name = "价格定位"
        verbose_name_plural=verbose_name






# 商品图片模型类
class GoodImage(models.Model):
    sku = models.ForeignKey('GoodSKU', verbose_name='产品')
    image = models.ImageField(upload_to='static/goods_img', verbose_name='图片路径')

    def __str__(self):
        return self.sku.name

    class Meta:
        db_table = 'good_image'
        verbose_name = '产品图片'
        verbose_name_plural = verbose_name





# 主页最上面的一幅 广告大图
class IndexAdd(models.Model):
    title = models.CharField(max_length=12, verbose_name='广告词')
    image = models.ImageField(upload_to='static/add_img', verbose_name='广告大图')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'index_add'
        verbose_name = '广告大图'
        verbose_name_plural = verbose_name





# 主页的三幅方形 广告中号图
class IndexAdd3(models.Model):
    title = models.CharField(max_length=12,verbose_name='广告中号标题')
    word = models.CharField(max_length=20,verbose_name='广告小号详情')
    image = models.ImageField(upload_to='static/add_img', verbose_name='广告中号图')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'index_add3'
        verbose_name = '首页三幅广告小图'
        verbose_name_plural = verbose_name













