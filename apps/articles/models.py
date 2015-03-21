# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import LiveArticleManager
from . import MultiSelectField


class Article(models.Model):
    BLOCK_CHOICES = [b[:2] for b in settings.ARTICLE_BLOCKS]

    # Fields
    block = MultiSelectField(_('Block'), max_length=1000, choices=BLOCK_CHOICES)
    title = models.CharField(_('Title'), max_length=250)
    description = models.TextField(_('Description'), null=True, blank=True)
    link = models.CharField(_('Link'), max_length=100, null=True, blank=True)
    file = models.FileField(_('File'), help_text=_('Image or flash file.'),
                            upload_to='/articles_files/', null=True, blank=True)
    file_caption = models.TextField(_('File Caption'), null=True, blank=True)
    video = models.CharField(_('Video'), max_length=400, null=True, blank=True)
    is_public = models.BooleanField(_('Is Public?'), default=True)
    pub_date = models.DateTimeField(_('Publication Date'), default=datetime.datetime.now)
    pub_end_date = models.DateTimeField(_('Publication End Date'), blank=True, null=True)
    creation_date = models.DateTimeField(_('Creation Date'), editable=False, default=datetime.datetime.now)

    # Managers
    objects = models.Manager()
    live_objects = LiveArticleManager()

    def __unicode__(self):
        return self.title
