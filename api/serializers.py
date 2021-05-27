from rest_framework import serializers
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
from django.contrib.auth.models import User

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['name', 'members', 'description']

class LabInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabInvite
        fields = ['invitee', 'lab_inviter', 'created_at', 'status']

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['lab', 'name', 'description']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['inventory', 'name', 'manufacturer', 'notes', 'quantity', 'minQuantity']

class ItemBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemBatch
        fields = ['item', 'expiryDate', 'quantity']

class ItemNoticesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemNotices
        fields = ['item', 'poster', 'text', 'created_at']

class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = ['item', 'orderRequester', 'quantityRequired', 'dateNeededBy', 'notes']

class ItemActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemActivityLog
        fields = ['action', 'item', 'user', 'quantity_changed', 'created_at']