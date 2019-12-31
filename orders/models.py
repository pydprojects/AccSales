from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from AccSales.tools import image_compressor
from home.models import BaseModel


def image_directory_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/<accounts_images>/<account_name>
    return "{0}/{1}".format('accounts_images', name)


class PSAccount(BaseModel):
    account_id = models.IntegerField(unique=True)
    email = models.EmailField(default=None, blank=True, null=True)
    owners = JSONField(default=None, blank=True, null=True)
    ex_owners = JSONField(default=None, blank=True, null=True)

    game = models.ForeignKey('Game', related_name='ps4accounts', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.account_id}'


class Game(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    system = models.CharField(max_length=16)
    cost = models.IntegerField()
    discount = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(95)])
    space = models.FloatField()
    region = models.CharField(max_length=64)
    image = models.ImageField(upload_to=image_directory_path, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def from_db(cls, db, field_names, values):
        new = super(Game, cls).from_db(db, field_names, values)
        # cache value went from the base
        new._loaded_image = values[field_names.index('image')]
        return new

    def save(self, *args, **kwargs):
        """If it is first save and there is no cached image but there is new one,
        or the value of image has changed"""
        if (self._state.adding and self.image) or \
                (not self._state.adding and self._loaded_image != self.image):
            compressed_image = image_compressor(image=self.image, name=self.name)
            self.image = compressed_image
        return super(Game, self).save(*args, **kwargs)
