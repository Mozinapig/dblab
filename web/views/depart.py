# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 18:12      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.shortcuts import render, redirect
from web import models
from web.utils.pagination import Pagination
from web.utils.form import UserModelForm, PrettyModelForm, PrettyEditModelForm


##
# Create your views here.
# 部门列表
def depart_list(request):

    queryset = models.Department.objects.all()
    page_obj = Pagination(request, queryset)
    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html()
    }

    return render(request, "depart_list.html", context)


# 添加部门
def depart_add(request):
    if request.method == "GET":
        return render(request, "depart_add.html")
    else:
        title = request.POST.get("title")
        models.Department.objects.create(title=title)
        return redirect("/depart/list/")


# 删除部门
def depart_delete(request):
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


# 编辑部门
def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    else:
        title = request.POST.get("title")
        models.Department.objects.filter(id=nid).update(title=title)
        return redirect("/depart/list/")

