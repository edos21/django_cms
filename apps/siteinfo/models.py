from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class SiteInfo(models.Model):
    title = models.CharField(_(u'Title'), max_length=200)
    subtitle = models.CharField(_(u'SubTitle'), max_length=200, blank=True, null=True)
    description = models.TextField(_(u'Description'), blank=True, null=True)
    logo = models.FileField(_(u'Logo'), upload_to='img/', blank=True, null=True)
    favicon = models.FileField(_(u'favicon'), upload_to='img/', blank=True, null=True)
    base_css = models.FileField(_(u'Base CSS'), upload_to='css/', blank=True, null=True)

    def __unicode__(self):
        return "%s, %s" % (self.title, self.subtitle)

    @property
    def get_stores(self):
        stores = Store.objects.filter(site=self).order_by('id')
        return stores


class Store(models.Model):
    site = models.ForeignKey(SiteInfo)
    name = models.CharField(_(u'Name'), max_length=200)
    phone = models.CharField(_(u'Phone'), max_length=50, blank=True, null=True)
    email = models.EmailField(_(u'Email'), blank=True, null=True)
    facebook_url = models.CharField(_(u'Facebook'), max_length=200, blank=True, null=True)
    twitter_url = models.CharField(_(u'Twitter'), max_length=200, blank=True, null=True)
    youtube_url = models.CharField(_(u'Youtube'), max_length=200, blank=True, null=True)
    googleplus_url = models.CharField(_(u'Google Plus'), max_length=200, blank=True, null=True)
    linkedin_url = models.CharField(_(u'Linkedin'), max_length=200, blank=True, null=True)
    address = models.TextField(_(u'Address'), blank=True, null=True)
    altitude = models.CharField(_(u'Altitude'), max_length=200, blank=True, null=True)
    latitude = models.CharField(_(u'Latitude'), max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name
