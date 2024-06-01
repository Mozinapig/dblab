# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/6/1 15:45      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""

from django.shortcuts import render,redirect
from django import forms

from web.utils.BootStrapModelForm import BootStrapForm
from web.utils.encrypt import md5
from web import models


class LoginForm(BootStrapForm):
    username = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True))

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 去数据库校验
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {"form": form})

        # 输入正确后操作,cookie和session
        # 网站生成随机字符串,写入用户浏览器的cookie中,再写入session中
        request.session["info"] = {"id": admin_object.id, "name": admin_object.username}
        return redirect('/admin/list/')

    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/login/')