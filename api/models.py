from django.db import models
from simple_history.models import HistoricalRecords
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

    @property
    def labItems(self):
        labInventories = self.inventory.all()
        querysets = []
        for inventory in labInventories:
            querysets.append(inventory.item.all())
        qsx = Lab.objects.none()
        for qs in querysets:
            qsx = qsx | qs
        return list(map(lambda item: item.id, qsx))


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


class ItemQuantityModel(models.Model):
    class Meta:
        abstract = True

    @property
    def quantity(self):
        itemBatches = self.itemBatch.all()
        totalStock = 0
        for itemBatch in itemBatches:
            totalStock += itemBatch.quantity
        return totalStock


class Item(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="item")
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    notes = models.TextField()
    quantity = models.IntegerField(default=0)
    minQuantity = models.IntegerField()
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    def setQuantity(self):
        itemBatches = self.itemBatch.all()
        totalStock = 0
        for itemBatch in itemBatches:
            totalStock += itemBatch.quantity
        self.quantity = totalStock

    def save(self, *args, **kwargs):
        self.setQuantity()
        if self.pk is not None:
            mostRecentHistory = self.history.most_recent()
            if mostRecentHistory.quantity == None:
                mostRecentHistory.quantity = 0
            if self.quantity > mostRecentHistory.quantity:
                diff = self.quantity - mostRecentHistory.quantity
                self._change_reason = "Increase by {}".format(diff)
            elif self.quantity < mostRecentHistory.quantity:
                diff = mostRecentHistory.quantity - self.quantity
                self._change_reason = "Decrease by {}".format(diff)
        super().save(*args, **kwargs)


class ItemBatch(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="itemBatch")
    expiryDate = models.DateField()
    quantity = models.IntegerField()
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.delete()
        else:
            super().save(*args, **kwargs)
        self.item.save()


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
