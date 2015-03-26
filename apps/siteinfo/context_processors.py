# -*- coding: utf-8 -*-
from .models import SiteInfo

def site_info(request):
	site = SiteInfo.objects.last()
	return {
            'site':site,
        }
