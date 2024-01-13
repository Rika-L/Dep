from django.shortcuts import render, HttpResponse, redirect
from employee_management.utils.modelform import BootStrapForm
from django import forms
from employee_management.utils.encrypt import md5
from employee_management.models import Admin
from employee_management.utils.code import check_code
from django.shortcuts import HttpResponse
from io import BytesIO


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(),
        required=True,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(),
        required=True,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    # 是否为空
    if form.is_valid():
        # 验证码的校验
        user_input_code = form.cleaned_data.pop('code')
        image_code = request.session.get('image_code', "")
        print(user_input_code, image_code)
        if image_code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'login.html', {'form': form})

        # 数据库查询数据
        admin_object = Admin.objects.filter(**form.cleaned_data).first()
        # 如果没有查询到数据
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 如果用户名密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie，再写道服务器的session中
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        # 重新设置超时时间
        request.session.set_expiry(60 * 60 * 24)
        return redirect("/admin/list/")
    return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    # 清除当前session
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """ 生成图片验证码 """
    # 调用pillow函数,生成图片
    img, code_string = check_code()

    # 写入到自己的session中
    request.session['image_code'] = code_string
    # 给session设置超时
    request.session.set_expiry(60)

    # 将图片保存到内存
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
