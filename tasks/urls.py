from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', home, name='home'),
    path('tasks/', tasks, name='tasks'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('tasks/create', create_task, name="create_task"),
    path('tasks/<int:task_id>', task_detail, name="task_detail"),
]