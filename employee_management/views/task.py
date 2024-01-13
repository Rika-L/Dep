from django.shortcuts import render, HttpResponse


def task_list(request):
    return render(request, 'task_list.html')


def task_ajax(request):
    print(request.GET)
    return HttpResponse('成功了')
