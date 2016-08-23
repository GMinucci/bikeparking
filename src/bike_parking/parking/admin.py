from django.contrib import admin
from . import models


class ParkingSpaceInline(admin.TabularInline):
    model = models.ParkingSpace
    extra = 0
    max_num = 100


class ParkingLotAdmin(admin.ModelAdmin):
    model = models.ParkingLot
    inlines = [ParkingSpaceInline, ]


admin.site.register(models.Location)
admin.site.register(models.Bicycle)
admin.site.register(models.ParkingLot, ParkingLotAdmin)
admin.site.register(models.ParkingSpace)

