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
    h_candidates = [(i, "%d:00"%i) for i in (11,21)]
    hour = models.IntegerField(choices=h_candidates, verbose_name='Time you\'ll arrive')
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
    category = models.ForeignKey('TableType', on_delete=models.CASCADE, null=False)

    # Shows up in the admin list
    def __str__(self):
        return "%s %s (contain %d~%d diners)"%(self.category.name, self.name, 
            self.category.min_person, self.category.max_person)