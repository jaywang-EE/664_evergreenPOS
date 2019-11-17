from django.db import models
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

class Order(models.Model) :
    custom = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Your name must be greater than 2 characters")]
    )
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    delivered = models.BooleanField(blank=True, default=False)
    
    def __str__(self):
        return self.custom

class MealNum(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)
    meal  = models.ForeignKey('Meal', on_delete=models.CASCADE, null=False)
    num   = models.IntegerField()
    def __str__(self):
        return "%s: %d"%(self.meal, self.num)

class Meal(models.Model):
    name = models.CharField(max_length=40)
    image_url = models.CharField(max_length=60)
    introdution = models.CharField(max_length=200)
    price = models.FloatField()
    calories = models.FloatField()
    protein = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    
    def __str__(self):
        return self.name
