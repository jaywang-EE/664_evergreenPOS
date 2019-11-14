from django.db import models
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

class Reserve(models.Model) :
    custom = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Your name must be greater than 2 characters")]
    )
    date = models.DateField()
    hour = models.IntegerField(validators=[MaxValueValidator(8), MinValueValidator(0)], 
                               verbose_name= 'Time(0~8, means 0 p.m. ~ 8 p.m.)')
    person     = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], 
                                     verbose_name= 'Number of diners')
    table      = models.ForeignKey('Table', on_delete=models.CASCADE, null=False)
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.custom

class TableType(models.Model):
    name = models.CharField(max_length=200)
    min_person = models.IntegerField()
    max_person = models.IntegerField()
    def __str__(self):
        return self.name

class Table(models.Model):
    name = models.CharField(max_length=200)
    
    # Shows up in the admin list
    def __str__(self):
        return "%s (contain %d~%d diners)"%(self.name, self.min_person, self.max_person)