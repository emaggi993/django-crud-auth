from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', home, name='home'),
    path('tasks/', tasks, name='tasks'),
    path('tasks_completed/', tasks_completed, name='tasks_completed'),
    path('logout/', signout, name='logout'),
    path('signin/', signin, name='signin'),
    path('tasks/create', create_task, name="create_task"),
    path('tasks/<int:task_id>', task_detail, name="task_detail"),
    path('tasks/<int:task_id>/completed', task_completed, name="task_completed"),
    path('tasks/<int:task_id>/deleted', task_deleted, name="task_deleted"),
]