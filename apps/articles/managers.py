# -*- coding: utf-8 -*-
from django.utils import timezone  # http://stackoverflow.com/a/21038922/1503
from django.db import models
from django.db.models import Q


class LiveArticleManager(models.Manager):

    def get_queryset(self):
        queryset = super(LiveArticleManager, self).get_queryset()
        now = timezone.now()
        in_range = Q(pub_date__lte=now) & (Q(pub_end_date__isnull=True) | Q(pub_end_date__gte=now))

        queryset = queryset.filter(in_range, is_public=True)

        return queryset
