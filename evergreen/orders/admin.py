from django.contrib import admin
from orders.models import Order, Meal, MealNum

# Register your models here.

admin.site.register(Meal)
admin.site.register(MealNum)
admin.site.register(Order)
