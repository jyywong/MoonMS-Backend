from django.contrib import admin
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
# Register your models here.
admin.site.register(Lab)
admin.site.register(LabInvite)
admin.site.register(Inventory)
admin.site.register(Item)
admin.site.register(ItemBatch)
admin.site.register(ItemNotices)
admin.site.register(ItemOrder)
admin.site.register(ItemActivityLog)
