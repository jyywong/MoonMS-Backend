from django.db import models
from moonMS import settings
# Create your models here.


class Lab(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='labs')
    description = models.TextField()

    def __str__(self):
        return self.name

    def removeMember(self, member):
        self.members.remove(member)


class LabInvite(models.Model):
    invitee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_invite')
    lab_inviter = models.ForeignKey(
        Lab, on_delete=models.CASCADE, related_name='lab_invite')
    created_at = models.DateField(auto_now=True)
    status_choices = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
    ]
    status = models.CharField(
        max_length=100,
        choices=status_choices,
        default='Pending'
    )

    def AcceptInvite(self):
        self.lab_inviter.members.add(self.invitee)


class Inventory(models.Model):
    lab = models.ForeignKey(
        Lab, on_delete=models.CASCADE, related_name="inventory")
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Item(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="item")
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    notes = models.TextField()
    quantity = models.IntegerField(blank=True, null=True)
    minQuantity = models.IntegerField()

    def __str__(self):
        return self.name


class ItemBatch(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemBatch")
    expiryDate = models.DateField()
    quantity = models.IntegerField()


class ItemNotices(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemNotices")
    poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class ItemOrder(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemOrders")
    orderRequester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantityRequired = models.IntegerField()
    dateNeededBy = models.DateField()
    notes = models.TextField()


class ItemActivityLog(models.Model):
    action_choices = [
        ('Add', 'Add'),
        ('Remove', 'Remove'),
    ]
    action = models.CharField(
        max_length=100,
        choices=action_choices,
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemActivity")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user')
    quantity_changed = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
