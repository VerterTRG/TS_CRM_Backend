from django.db import models
from django.contrib.auth.models import AbstractUser

# AUTH_USER_MODEL = 'yourapp.CustomUser' to setting

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'crm_users'

    def __str__(self):
        return self.username
    
    # def __new__(cls) -> 'User':
    #     return super().__new__(cls)