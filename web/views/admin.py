# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 23:31      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.shortcuts import render

from web import models
from web.utils.pagination import Pagination

def admin_list(request):
    #搜索
    search_data = request.GET.get('q', "")
    data_dict = {}
    if search_data:
        data_dict["username__contains"] = search_data

    #根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)
    #分页
    page_object = Pagination(request,queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string":page_object.html(),
        "search_data":search_data,
    }

    return render(request, "admin_list.html", context)
