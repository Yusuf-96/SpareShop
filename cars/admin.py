from django.contrib import admin
from .models import Car
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    list_display = (
        'car_name', 'engine_no', 'car_model'
    )


admin.site.register(Car, CarAdmin)

