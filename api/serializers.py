from rest_framework import serializers
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, *args, **kwargs):
        new_user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password2': 'Passwords must match'})

        new_user.set_password(password)
        new_user.save()
        return new_user


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'name', 'members', 'description']


class LabInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabInvite
        fields = ['invitee', 'lab_inviter', 'created_at', 'status']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'lab', 'name', 'description']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['inventory', 'name', 'manufacturer',
                  'notes', 'quantity', 'minQuantity']


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
        fields = ['item', 'orderRequester',
                  'quantityRequired', 'dateNeededBy', 'notes']


class ItemActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemActivityLog
        fields = ['action', 'item', 'user', 'quantity_changed', 'created_at']
