from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'name', 'type', 'dealer_id')
    list_filter = ['name', 'car_make', 'type', 'dealer_id']
    search_fields = ['name']

# CarMakeAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)