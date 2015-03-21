# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import unordered_list

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', '_block', 'is_public', 'pub_date')
    list_filter = ('block', 'creation_date', 'pub_date', 'is_public')
    date_hierarchy = 'pub_date'
    search_fields = ('title', 'block', )
    fieldsets = (
        (None, {'fields': ('title', 'block', 'file', 'file_caption', 'link', 'video', 'description')}),
        (_('Visualisation settings'), {'fields': ('is_public', 'pub_date', 'pub_end_date')}),
    )

    def _block(self, object):
        items = unordered_list(['%s' % (name,) for key, name in Article.BLOCK_CHOICES if key in object.block])
        return '<ul>%s</ul>\n' % items
    _block.short_description = _('block')
    _block.allow_tags = True