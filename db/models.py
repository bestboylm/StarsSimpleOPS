from django.db import models

# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(verbose_name='名字', max_length=32, db_index=True)
    password = models.CharField(verbose_name='密码', max_length=256,null=False)
    email = models.EmailField(verbose_name='邮箱', unique=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(verbose_name='名字', max_length=32, null=False)
    command = models.CharField(verbose_name='发布命令', max_length=256,)

    class Meta:
        verbose_name_plural = '项目表'

    def __str__(self):
        return self.name


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField('机房', max_length=32)
    floor = models.IntegerField('楼层', default=1)

    class Meta:
        verbose_name_plural = "机房表"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, '在线'),
        (2, '离线'),
    )

    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.CharField('机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField('机柜中序号', max_length=30, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    business = models.ForeignKey('Business', verbose_name='属于的业务线', null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产表"

    def __str__(self):
        return "%s-%s-%s" % (self.idc.name, self.cabinet_num, self.cabinet_order)


class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset')

    hostname = models.CharField(max_length=128, unique=True)
    sn = models.CharField('SN号', max_length=64, null=True, db_index=True)
    model = models.CharField('型号', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField('管理IP', null=True, blank=True, db_index=True)

    os_platform = models.CharField('系统', max_length=16, null=True, blank=True)
    os_version = models.CharField('系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField('CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField('CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField('CPU型号', max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname