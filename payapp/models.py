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