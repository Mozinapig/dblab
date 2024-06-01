# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/6/1 17:33      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除不需要登录就能访问的页面
        # 获取当前用户请求的url
        if request.path_info == '/login/':
            return

        # 1.读取当前用户的session信息
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 2.没有登录信息,回到登录页面
        return redirect('/login/')
