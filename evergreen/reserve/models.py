from django.db import models
from django.core.validators import MinLengthValidator,MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

class Reserve(models.Model) :
    custom = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Your name must be greater than 2 characters")]
    )
    time       = models.DateTimeField()
    table      = models.ForeignKey('Table', on_delete=models.CASCADE, null=False)
    phone      = models.CharField(max_length=20)
    person     = models.IntegerField(verbose_name= 'Number of diners')
    owner      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Shows up in the admin list
    def __str__(self):
        return "Table %s"%(self.table)

class TableType(models.Model):
    name = models.CharField(max_length=200)
    min_person = models.IntegerField()
    max_person = models.IntegerField()
    
    def range(self): return "%d~%d"%(self.min_person, self.max_person)
    def range_full(self): return "(contain %s diners)"%self.range
    def valid(self, num): 
        if num > self.max_person:
            return "%s table can only contain %d diners"%(self.name, self.max_person)
        elif num < self.min_person: 
            return "%s table should have at least %d diners"%(self.name, self.min_person)
        else: return ""

    def __str__(self): return self.name

class Table(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey('TableType', on_delete=models.CASCADE, null=False)

    def valid(self, num): return self.category.valid(num)
    # Shows up in frontEnd
    def show(self): return "%s %s"%(self.category.name, self.name)
    # Shows up in the admin list
    def __str__(self): return self.show()