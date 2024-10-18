from django.db import models

# Create your models here.

class UserData(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username