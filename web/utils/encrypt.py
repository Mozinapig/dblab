# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/6/1 10:26      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
import hashlib

from django.conf import settings


def md5(data_string):
    # 加盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
