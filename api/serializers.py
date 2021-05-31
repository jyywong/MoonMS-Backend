from django.db.models import query
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    labs = PrimaryKeyRelatedField(many=True, queryset=Lab.members)

    class Meta:
        model = User
        fields = ['id', 'username', 'labs']


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
    inventories = serializers.PrimaryKeyRelatedField(source="inventory",
                                                     many=True, queryset=Inventory.objects.all())

    class Meta:
        model = Lab
        fields = ['id', 'name', 'members', 'description', 'inventories']


class LabInviteSerializer(serializers.ModelSerializer):
    inviteeEmail = serializers.EmailField(write_only=True)

    class Meta:
        model = LabInvite
        fields = ['inviteeEmail', 'lab_inviter', 'created_at', 'status']

    def create(self, validated_data):
        print(validated_data['inviteeEmail'])
        print(User.objects.filter(email=validated_data['inviteeEmail']))
        print(User.objects.filter(
            email=validated_data['inviteeEmail']).exists())
        if User.objects.filter(email=validated_data['inviteeEmail']).exists():
            print('HELOOOOOOOO')
            targetUser = User.objects.get(email=validated_data['inviteeEmail'])
            newLabInvite = LabInvite.objects.create(
                invitee=targetUser, lab_inviter=validated_data['lab_inviter'], status='Pending')
            newLabInvite.save()
            return newLabInvite


class InventorySerializer(serializers.ModelSerializer):
    labID = serializers.PrimaryKeyRelatedField(
        source="lab", queryset=Lab.objects.all())
    items = serializers.PrimaryKeyRelatedField(
        source="item", many=True, queryset=Item.objects.all())

    class Meta:
        model = Inventory
        fields = ['id', 'labID', 'name', 'description', 'items']


class ItemSerializer(serializers.ModelSerializer):
    invID = serializers.PrimaryKeyRelatedField(
        source="inventory", queryset=Item.objects.all())
    notices = serializers.PrimaryKeyRelatedField(
        source="itemNotices", many=True, queryset=ItemNotices.objects.all())

    class Meta:
        model = Item
        fields = ['id', 'invID', 'name', 'manufacturer',
                  'notes', 'quantity', 'minQuantity', 'notices']


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
