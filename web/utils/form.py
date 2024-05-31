# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 18:05      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""

from web import models
from web.utils.BootStrapModelForm import BootStrapModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'time', 'depart', 'gender']


class PrettyModelForm(BootStrapModelForm):
    # 解决格式问题,进行格式校验,正则表达式
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def clean_mobile(self):  # 判断手机号是否存在
        text_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return text_mobile


class PrettyEditModelForm(BootStrapModelForm):
    # 解决格式问题,进行格式校验,正则表达式
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def clean_mobile(self):  # 判断手机号是否存在【排除自己还有无此手机号】
        text_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return text_mobile
