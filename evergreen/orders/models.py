from django.db import models
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

class Order(models.Model) :
    custom = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Your name must be greater than 2 characters")]
    )
    owner        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone        = models.CharField(max_length=12)
    addr         = models.CharField(max_length=100)
    created_at   = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)
    delivered    = models.BooleanField(default=False)
    
    def __str__(self):
        return self.custom

class MealNum(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=False)
    meal  = models.ForeignKey('Meal', on_delete=models.CASCADE, null=False)
    num   = models.IntegerField()

    def __radd__(self, y): # sum
        return y + self.num*self.meal.price

    def __str__(self):
        return "%s: %d"%(self.meal, self.num)

class Nutrition():
    def __init__(self, meal, num):
        self.num = num
        self.price = meal.price*num
        self.calories = meal.calories*num
        self.protein = meal.protein*num
        self.carbohydrates = meal.carbohydrates*num
        self.fat = meal.fat*num
        
    def ratio(self):
        return {"calories":toperc(self.calories/2400), "carbohydrates":toperc(self.carbohydrates/225.0), "fat":toperc(self.fat/60.0)}

def toperc(n):
    return int(n*100)

class Meal(models.Model):
    name = models.CharField(max_length=40)
    image_url = models.CharField(max_length=60)
    introdution = models.CharField(max_length=200)
    price = models.FloatField()
    calories = models.FloatField()
    protein = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    fat = models.FloatField(null=True)

    def ratio(self):
        return {"calories":toperc(self.calories/2400), "carbohydrates":toperc(self.carbohydrates/225.0), "fat":toperc(self.fat/60.0)}
    
    def __lt__(self, ml):
        return self.name<ml.name
    def __gt__(self, ml):        
        return self.name>ml.name

    def __mul__(self, n):
        return Nutrition(self, n)
    
    def __str__(self):
        return self.name
