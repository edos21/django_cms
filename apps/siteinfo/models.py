from django.db import models

# Create your models here.


class BaseInfo(models.Model):
    title = models.CharField(verbose_name='Title', max_length=200)
    subtitle = models.CharField(verbose_name='SubTitle', max_length=200)
