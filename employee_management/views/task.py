import json
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from employee_management.utils.modelform import BootStrapModelForm
from employee_management import models
from django import forms


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            "detail": forms.TextInput,
            "title": forms.TextInput(attrs={'placeholder': '标题'})
        }


@csrf_exempt
def task_list(request):
    """任务列表"""
    form = TaskModelForm()
    return render(request, 'task_list.html', {'form': form})


@csrf_exempt
def task_add(request):
    # print(request.POST)

    # 进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dist = {'status': True}
        return HttpResponse(json.dumps(data_dist))

    data_dist = {'status': False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dist, ensure_ascii=False))
