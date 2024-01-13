from django.shortcuts import render, redirect
from employee_management.models import Department, UserInfo
from employee_management.utils.pagination import Pagination
from employee_management.form.form import UserModelFrom


def user_list(request):
    """用户列表"""

    queryset = UserInfo.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }

    return render(request, 'user_list.html', context)


def user_add(request):
    """用户添加"""
    if request.method == 'GET':
        context = {
            'gender_choices': UserInfo.gender_choices,
            'depart_list': Department.objects.all(),
        }
        return render(request, 'user_add.html', context)
    username = request.POST.get('username')
    password = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    depart_id = request.POST.get('depart')
    gender_id = request.POST.get('gender')
    # print(username, password, age, account, create_time, depart, gender)
    UserInfo.objects.create(name=username, password=password,
                            age=age, account=account, create_time=create_time,
                            gender=gender_id, depart_id=depart_id)
    return redirect('/user/list/')


def user_delete(request):
    """用户删除"""
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def user_model_form_add(request):
    """添加用户（modelform版本）"""
    if request.method == "GET":
        form = UserModelFrom()
        return render(request, 'user_model_form_add.html', {'form': form})

    # 用户数据校验
    form = UserModelFrom(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    # 检验失败，在页面上显示错误信息
    return render(request, 'user_model_form_add.html', {'form': form})


def user_edit(request, nid):
    """用户编辑"""
    row_object = UserInfo.objects.filter(id=nid).first()
    # 根据id获取编辑行得数据
    if request.method == 'GET':
        form = UserModelFrom(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    # 用户数据校验
    form = UserModelFrom(data=request.POST, instance=row_object)
    # print(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

        # 检验失败，在页面上显示错误信息
    return render(request, 'user_edit.html', {'form': form})
