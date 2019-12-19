from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Roles(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    moderation = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ExtendedUserData(BaseModel):
    """Extended User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.username
