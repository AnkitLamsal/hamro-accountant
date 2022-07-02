from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Accountant(models.Model):
    accountant = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.accountant}'
    
class Position(models.Model):
    position_name = models.CharField(max_length=50, unique=True)
    position_details = models.TextField(max_length=200, null=True)
    base_salary = models.PositiveIntegerField()
    tada = models.FloatField(default = 10000, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f'{self.position_name}'

class Employee(models.Model):
    position = models.ForeignKey(Position, on_delete= models.PROTECT)
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    accountant = models.ForeignKey(Accountant, on_delete= models.CASCADE)
    pf_percent = models.FloatField(default=10.0,validators=[MinValueValidator(10.0),MaxValueValidator(20.0)])    
    strip_account_id = models.CharField(max_length=100,blank=True, null=True)
    def __str__(self):
        return f'{self.employee}'
    
