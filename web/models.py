from django.db import models


# Create your models here.
# 创建部门表
class Department(models.Model):
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


# 创建员工表
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=15, decimal_places=6, default=0)
    time = models.DateTimeField(verbose_name="入职时间")
    depart = models.ForeignKey("Department", on_delete=models.CASCADE, verbose_name='部门')  # 自动加id变为depart_id,设置级联删除
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
