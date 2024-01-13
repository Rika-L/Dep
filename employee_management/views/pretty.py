from django.shortcuts import render, redirect
from employee_management.models import PrettyNum
from employee_management.utils.pagination import Pagination
from employee_management.form.form import PrettyModelForm, PrettyEditModelForm


# 靓号管理部分

def pretty_list(request):
    """靓号列表"""

    """纯代码实现分页"""
    # 插入测试数据
    # for i in range(600):
    #    PrettyNum.objects.create(mobile="13811223344", price=100, level=3, status=1)

    data_dict = {}
    search_data = request.GET.get('query', "")
    if search_data:
        # mobile_contains 表示筛选出字段mobile包含 search_data 数据的行
        data_dict["mobile__contains"] = search_data

    queryset = PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 实例化
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "search_data": search_data,
        'page_string': page_object.html()  # 页码
    }

    return render(request, 'pretty_list.html', context)


def pretty_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


def pretty_edit(request, nid):
    """靓号编辑"""
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        print(row_object)
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """靓号删除"""
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
