from django.contrib import admin

from .models import (
    City,
    Consulation,
    MarakezMoshavere,
    MoshaverProfile,
    Daneshkadeh,
    Reservation,
    Days,
    Nobat,
    Time
)


@admin.register(Consulation)
class ConsulationAdmin(admin.ModelAdmin):
    pass


@admin.register(MarakezMoshavere)
class MarakezMoshavereAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(MoshaverProfile)
class MoshaverProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Daneshkadeh)
class DaneshkadehAdmin(admin.ModelAdmin):
    pass

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass


@admin.register(Days)
class DaysAdmin(admin.ModelAdmin):
    pass

@admin.register(Nobat)
class NobatAdmin(admin.ModelAdmin):
    pass

@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    pass
