from django.db import models
from django.urls import reverse

from Image.steno_encryption import steno_encrypt

# Create your models here.


class Image(models.Model):
    caption = models.CharField(max_length=100, null=False)
    image = models.ImageField(blank=False, null=False, upload_to='Image')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        super(Image, self).save()
        steno_encrypt(kwargs['key'], kwargs['msg'], self.image.path)
        print(kwargs)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.image.path
