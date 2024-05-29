from django.shortcuts import render, redirect
from web import models


# Create your views here.
# 部门列表
def depart_list(request):
    queryset = models.Department.objects.all()
    return render(request, "depart_list.html", {"queryset": queryset})


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


def depart_edit(request, nid):
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"row_object": row_object})
    else:
        title = request.POST.get("title")
        models.Department.objects.filter(id=nid).update(title=title)
        return redirect("/depart/list/")


# 用户管理
def user_list(request):
    queryset = models.UserInfo.objects.all()

    return render(request, "user_list.html", {"queryset": queryset})


from django import forms


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'time', 'depart', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_add.html", {"form": form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

