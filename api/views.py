from django.db.models import query
from django.shortcuts import render
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
from .serializers import UserSerializer, RegisterUserSerializer, LabSerializer, LabInviteSerializer, InventorySerializer, ItemSerializer, ItemBatchSerializer, ItemNoticesSerializer, ItemOrderSerializer, ItemActivityLogSerializer
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def api_registration_view(request):
    serializer = RegisterUserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        new_user = serializer.save()
        data['response'] = 'Successfully created new user'
        data['username'] = new_user.username
        data['email'] = new_user.email
    else:
        data = serializer.errors
    return Response(data)
# Create your views here.


class lab_list(generics.ListCreateAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer


class lab_invite_list(generics.ListCreateAPIView):
    queryset = LabInvite.objects.all()
    serializer_class = LabInviteSerializer


class inventory_list(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


class item_list(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class item_batch_list(generics.ListCreateAPIView):
    queryset = ItemBatch.objects.all()
    serializer_class = ItemBatchSerializer


class item_notices_list(generics.ListCreateAPIView):
    queryset = ItemNotices.objects.all()
    serializer_class = ItemNoticesSerializer


class item_order_list(generics.ListCreateAPIView):
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer


class item_activity_log_list(generics.ListCreateAPIView):
    queryset = ItemActivityLog.objects.all()
    serializer_class = ItemActivityLogSerializer
