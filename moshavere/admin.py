from django.contrib import admin
from .models import Employee, Consulation

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Consulation)
class ConsulationAdmin(admin.ModelAdmin):
    pass