from django.contrib import admin

from .models import (City, Consulation, MarakezMoshavere,
                     MoshaverProfile, Daneshkadeh, Nazer, Reservation)


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

@admin.register(Nazer)
class NazerAdmin(admin.ModelAdmin):
    pass

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
