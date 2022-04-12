from django.contrib import admin

from .models import City, Consulation, Employee, MarakezMoshavere


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Consulation)
class ConsulationAdmin(admin.ModelAdmin):
    pass

@admin.register(MarakezMoshavere)
class MarakezMoshavereAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
