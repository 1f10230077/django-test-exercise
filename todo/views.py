from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
import random


# Create your views here.
def index(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_at_str = request.POST['due_at']
        memo = request.POST.get('memo' ,'')        
        if title and due_at_str:
            due_at = make_aware(parse_datetime(due_at_str))
            task = Task(title=title, due_at=due_at, memo = memo)
            task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def update(request, task_id):
    try:
        task = Task.objects.get(pk = task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.memo = request.POST['memo']
        task.save()
        return redirect(detail, task_id)
    context = {
        'task' : task,
    }
    return render(request, 'todo/edit.html', context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.delete()
    return redirect('index')

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect('omikuji')

def OMIKUJI(request):
    fortune = random.randint(1, 6)
    fortuneMessage = ''

    if fortune == 1:
        fortuneMessage = '大吉'
    elif fortune == 2 or fortune == 3:
        fortuneMessage = '吉'
    elif fortune == 4 or fortune == 5:
        fortuneMessage = '小吉'
    elif fortune == 6:
        fortuneMessage = '凶'

    data = {
        'fortune':fortuneMessage
    }
    return render(request, 'todo/omikuji.html', data)