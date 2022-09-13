from django.contrib import admin
from .models import Task

#para modificar el panel de administrador para que muestre los campos de solo lectura
class TaskAdmin(admin.ModelAdmin):
    readonly_fields= ("created",)


#registro al panel de administracion
admin.site.register(Task, TaskAdmin)
