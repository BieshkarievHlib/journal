from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class StandardUser(AbstractUser):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def __str__(self):
        return self.surname + self.name