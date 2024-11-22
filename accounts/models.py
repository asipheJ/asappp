from django.db import models

class Account(models.Model):
    account_number = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    id_number = models.CharField(max_length=20)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=256)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
