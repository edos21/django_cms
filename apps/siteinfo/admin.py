from django.contrib import admin
from .models import SiteInfo, Store
# Register your models here.


class StoreInline(admin.StackedInline):
    model = Store
    extra = 1


@admin.register(SiteInfo)
class SiteAdmin(admin.ModelAdmin):
    inlines = [
        StoreInline,
    ]