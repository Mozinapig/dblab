# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 18:13      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


# 用户管理
def user_list(request):
    queryset = models.UserInfo.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }

    return render(request, "user_list.html", context)


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")


def user_edit(request, nid):
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = UserModelForm(instance=row_obj)
        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, 'user_edit.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
