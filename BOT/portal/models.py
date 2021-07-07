from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
# Create your models here.



def __str__(self):
		return "Proctor Form of user {}".format(self.created.username)
