from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
import traceback
# Create your views here.


def signup(request):
    if request.method == 'GET':

        return render(request, "signup.html", {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/tasks/')
            except:
                return render(request, "signup.html", {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, "signup.html", {
                'form': UserCreationForm,
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull= True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user= request.user, datecompleted__isnull= False).order_by('-datecompleted')
    return render(request, 'tasks_completed.html', {
        'tasks': tasks
    })

def home(request):
    return render(request, 'home.html')

@login_required
def signout(request):
    logout(request)
    return redirect("/")
def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        try:
            user = authenticate( request, username= request.POST['username'], password= request.POST['password'])
            if user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'usuario o contraseña incorrecta'
                })
            else:
                login(request, user)
                return redirect('/tasks')
        except:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': traceback.format_exc()
            })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form= TaskForm(request.POST)
            new_task= form.save(commit=False)
            new_task.user = request.user
            print(new_task)
            new_task.save()
            
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': "Ingrese datos correctos"
            })
        else:
            return redirect("tasks")
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'GET':
        form= TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'form': form,
            'task': task
        })
    else:
        try:
            form= TaskForm(request.POST,instance=task)
            form.save()
        
        except ValueError:
            return render(request, 'task_detail.html', {
                'form': form,
                'error': "Ocurrio un error al actualizar el sistema",
                'task': task
            })
        else:
            return redirect('tasks')

@login_required
def task_completed(request, task_id):
    task = get_object_or_404(Task, pk= task_id, user= request.user)
    if request.method ==  'POST':
        try:
            task.datecompleted = timezone.now()
            task.save()
        except ValueError:
            return render(request, 'task_detail.html', {
                
                'error': "Ocurrio un error al actualizar el sistema",
                'task': task
            })
        else:
            return redirect('tasks')
@login_required
def task_deleted(request, task_id):
    task = get_object_or_404(Task, pk= task_id, user= request.user)
    if request.method ==  'POST':
        try:
            task.delete()
        except ValueError:
            return render(request, 'task_detail.html', {
                
                'error': "Ocurrio un error al actualizar el sistema",
                'task': task
            })
        else:
            return redirect('tasks')