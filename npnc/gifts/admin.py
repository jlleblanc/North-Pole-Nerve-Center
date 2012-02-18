from django.contrib import admin
from npnc.gifts.models import WishItem

class WishItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(WishItem, WishItemAdmin)
