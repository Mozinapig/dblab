from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from web import models


##
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


# 编辑部门
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


# 创建UserInfo表的ModelForm
# Modedlform
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


def pretty_list(request):
    search_data = request.GET.get('q',"")
    data_dict={}
    if search_data:
        data_dict["mobile__contains"]=search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")  # 按照级别从大到小排序
    return render(request, "pretty_list.html", {"queryset": queryset,"search_data":search_data})


from django.core.validators import RegexValidator


class PrettyModelForm(forms.ModelForm):
    # 解决格式问题,进行格式校验,正则表达式
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):  # 判断手机号是否存在
        text_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return text_mobile


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


class PrettyEditModelForm(forms.ModelForm):
    # 解决格式问题,进行格式校验,正则表达式
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_mobile(self):  # 判断手机号是否存在【排除自己还有无此手机号】
        text_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=text_mobile).exists()
        if exists:
            raise ValidationError('手机号已经存在')
        return text_mobile


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
