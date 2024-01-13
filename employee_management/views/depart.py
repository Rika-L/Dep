from django.shortcuts import render, redirect
from employee_management.models import Department
from employee_management.utils.pagination import Pagination


def depart_list(request):
    """部门列表"""
    queryset = Department.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """部门添加"""
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    depart_plus = request.POST.get('depart_plus')
    Department.objects.create(title=depart_plus)
    return redirect('/depart/list/')


def depart_delete(request):
    """部门删除"""
    nid = request.GET.get('nid')
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_edit(request, nid):
    """部门编辑"""
    if request.method == 'GET':
        row_object = Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})
    depart_plus = request.POST.get('depart_plus')
    Department.objects.filter(id=nid).update(title=depart_plus)
    return redirect('/depart/list')
