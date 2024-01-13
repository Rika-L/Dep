from django.shortcuts import render, redirect
from employee_management.models import Admin
from employee_management.utils.pagination import Pagination
from employee_management.utils.modelform import BootStrapModelForm
from django import forms
from django.core.exceptions import ValidationError
from employee_management.utils.encrypt import md5


def admin_list(request):
    """管理员列表"""
    queryset = Admin.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, 'admin_list.html', context)


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 钩子函数
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致')
        # return返回什么保存到数据库的就是什么
        return md5(confirm)


# 如果不想让用户修改密码，只修改用户名，那么使用下面的AdminEditModelForm类
# 如果都可以修改，直接用上面的AdminModelForm类
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    password = forms.CharField(
        label='新的密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = Admin
        fields = ["password", "confirm_password"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        exists = Admin.objects.filter(id=self.instance.pk, password=md5(pwd))
        if exists:
            raise ValidationError("密码不能与当前密码一致")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致')
        # return返回什么保存到数据库的就是什么
        return md5(confirm)


def admin_edit(request, nid):
    """编辑管理员"""
    # 判断nid是否存在
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'errors.html', {"msg": "数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form": form, "title": title})


def admin_add(request):
    """添加管理员"""
    title = "新建管理员"
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, 'title': title})
    form = AdminModelForm(data=request.POST)
    context = {
        "form": form,
        "title": title,
    }
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", context)


def admin_delete(request, nid):
    # 判断nid是否存在
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'errors.html', {"msg": "数据不存在"})
    """管理员删除"""
    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    """密码重置"""
    # 判断nid是否存在
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'errors.html', {"msg": "数据不存在"})

    title = "重置密码 - {}".format(row_object.username)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'title': title, 'form': form})
    form = AdminResetModelForm(instance=row_object, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {'title': title, 'form': form})
