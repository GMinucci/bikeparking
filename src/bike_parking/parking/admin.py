from django.contrib import admin
from . import models


class ParkingSpaceInline(admin.TabularInline):
    model = models.ParkingSpace
    extra = 0
    max_num = 100
    exclude = [
        'number',
    ]


class ParkingLotAdmin(admin.ModelAdmin):
    model = models.ParkingLot
    inlines = [ParkingSpaceInline, ]


class LocationAdmin(admin.ModelAdmin):
    model = models.Location
    fieldsets = (
        (None, {
            'fields': ('cep', 'street', 'number', 'neighborhood', 'city', 'state', 'country', 'complement')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('latitude', 'longitude', 'point'),
        }),
    )

admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Bicycle)
admin.site.register(models.ParkingLot, ParkingLotAdmin)
admin.site.register(models.ParkingSpace)
admin.site.register(models.Person)
admin.site.register(models.Rental)
admin.site.register(models.Payment)

