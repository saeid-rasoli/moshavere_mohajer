from django.contrib import admin

from .models import (City, Consulation, MarakezMoshavere,
                     ProfileEmployee, Daneshkadeh)


@admin.register(Consulation)
class ConsulationAdmin(admin.ModelAdmin):
    pass


@admin.register(MarakezMoshavere)
class MarakezMoshavereAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileEmployee)
class ProfileEmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Daneshkadeh)
class DaneshkadehAdmin(admin.ModelAdmin):
    pass
