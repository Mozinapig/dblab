# 数据库杨敏实验四  ——  联通用户管理系统
## 环境准备
1、确保安装Django与mysqlclient
```python
# pip install django
# pip install mysqlclient
```
2、创建dblab数据库
```mysql
# create database dblab;
```
3、将settings.py文件中密码改为自己密码
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dblab',  # 数据库名字
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',  # 本机
#         'PORT': 3306,  # 端口
#     }
# }
```
## 页面说明
```html
<!--depart/list/    部门列表-->
<!--depart/add/     添加部门-->
<!--depart/delete/  删除部门-->
<!--depart/<int:nid>/edit/  编辑部门-->
<!--user/list/  用户列表-->
<!--user/add/   添加用户-->
```