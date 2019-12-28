from django.contrib.postgres.fields import JSONField
from django.db import models

from home.models import BaseModel


def image_directory_path(name):
    # file will be uploaded to MEDIA_ROOT/<accounts_images>/<account_name>
    return "{0}/{1}".format('accounts_images', name)


class PSAccount(BaseModel):
    account_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=64, unique=False)
    email = models.EmailField(default=None, blank=True, null=True)
    owners = JSONField(default=None, blank=True, null=True)
    ex_owners = JSONField(default=None, blank=True, null=True)
    image = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return self.account_id, self.name, self.owners


# class Payment(BaseModel):
#     id = models.CharField()
#
#     def __str__(self):
#         return self.id
