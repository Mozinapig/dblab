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

def pretty_list(request):
    # for i in range(1,100):#测试代码
    #     models.PrettyNum.objects.create(mobile='13872185001',price=0,level=1,status=1)
    search_data = request.GET.get('q', "")
    data_dict = {}
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 新增分页功能
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "search_data": search_data,
        "page_string": page_object.html(),  # 生成的页码
    }

    return render(request, "pretty_list.html", context)


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 解决格式问题,进行格式校验
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "pretty_edit.html", {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")