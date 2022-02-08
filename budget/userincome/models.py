from django.db import models
from django.contrib.auth.models import User
from expenses.models import Budynek
from datetime import date

# Create your models here.
class UserIncome(models.Model):
    amount = models.FloatField()  # decimal
    waluta = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True, default=date.today)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    budynek = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']


class Source(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


