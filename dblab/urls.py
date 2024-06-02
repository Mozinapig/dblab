"""
URL configuration for dblab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views
from web.views import depart, user, pretty, admin, account

from django.urls import path, re_path
from django.views.generic import RedirectView

# 直接访问login
urlpatterns = [
    # path("admin/", admin.site.urls),
    path('', RedirectView.as_view(url='/login/')),
    path("depart/list/", depart.depart_list),
    path("depart/add/", depart.depart_add),
    path("depart/delete/", depart.depart_delete),
    path("depart/<int:nid>/edit/", depart.depart_edit),

    path("user/list/", user.user_list),
    path("user/add/", user.user_add),
    path("user/<int:nid>/edit/", user.user_edit),
    path("user/<int:nid>/delete/", user.user_delete),

    path("pretty/list/", pretty.pretty_list),
    path("pretty/add/", pretty.pretty_add),
    path("pretty/<int:nid>/edit/", pretty.pretty_edit),
    path("pretty/<int:nid>/delete/", pretty.pretty_delete),

    path("admin/list/", admin.admin_list),
    path("admin/add/", admin.admin_add),
    path("admin/<int:nid>/edit/", admin.admin_edit),
    path("admin/<int:nid>/delete/", admin.admin_delete),
    path("admin/<int:nid>/reset/", admin.admin_reset),

    path("login/", account.login),
    path("logout/", account.logout),

]
