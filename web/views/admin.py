# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 23:31      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.shortcuts import render, redirect

from web import models
from web.utils.pagination import Pagination


def admin_list(request):

    # 搜索
    search_data = request.GET.get('q', "")
    data_dict = {}
    if search_data:
        data_dict["username__contains"] = search_data

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data,
    }

    return render(request, "admin_list.html", context)


from django.core.exceptions import ValidationError
from django import forms

from web.utils.BootStrapModelForm import BootStrapModelForm
from web.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    # md5加密管理员密码
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username", ]


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        # 去数据库校验,密码不能和原来密码一样
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前一致!")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin_add(request):
    title = '管理员添加'
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change_add.html", {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 数据库存储的是md5密文
        form.save()
        return redirect('/admin/list/')

    return render(request, "change_add.html", {"form": form, "title": title})


def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": '数据不存在'})

    title = '编辑管理员'
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change_add.html", {'form': form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, "change_add.html", {'form': form, "title": title})


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg": '数据不存在'})

    title = '重置密码-{}'.format(row_object.username)
    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change_add.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 数据库存储的是md5密文
        form.save()
        return redirect('/admin/list/')

    return render(request, "change_add.html", {"form": form, "title": title})
