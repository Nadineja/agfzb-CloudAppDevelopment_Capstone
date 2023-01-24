from django.contrib import admin
from .models import CarModel, CarMake


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):

    list_display = ('dealership', 'name', 'make', 'model', 'year')
    search_fields = ['name', 'dealership', 'model']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description', 'date')
    search_fields = ['name', 'description']


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
