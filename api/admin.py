from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
# Register your models here.
admin.site.register(Lab)
admin.site.register(LabInvite)
admin.site.register(Inventory)
admin.site.register(Item, SimpleHistoryAdmin)
admin.site.register(ItemBatch, SimpleHistoryAdmin)
admin.site.register(ItemNotices)
admin.site.register(ItemOrder)
admin.site.register(ItemActivityLog)
