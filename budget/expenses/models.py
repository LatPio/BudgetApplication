from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Expense(models.Model):
    amount = models.FloatField()
    waluta = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True, default=date.today)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, default="Nie podano")
    budynek = models.CharField(max_length=255, blank=True, null=True)

    # currency = models.TextField(blank=True)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']

class Budynek(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


