import factory
from faker import Faker
from .models import Lab, LabInvite, Inventory, Item, ItemBatch, ItemNotices, ItemOrder, ItemActivityLog
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from random import choice

fake = Faker()
Faker.seed(0)


class UserFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyFunction(fake.name)
    password = factory.PostGenerationMethodCall(
        'set_password', fake.password())
    email = factory.LazyFunction(fake.email)


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lab

    name = factory.LazyFunction(fake.bs)
    # members = factory.LazyAttribute(lambda a: choice(
    #     get_user_model().objects.all()))
    description = factory.LazyAttribute(lambda a: fake.sentence(nb_words=5))

    # @factory.post_generation
    # def members(self, create, extracted,  **kwargs):
    #     if create:
    #         self.members.set(choice(User.objects.all()))


class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory
    lab = factory.LazyAttribute(lambda a: choice(Lab.objects.all()))
    name = factory.LazyFunction(fake.bs)
    description = factory.LazyAttribute(lambda a: fake.sentence(nb_words=5))


class ItemFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = Item
    inventory = factory.LazyAttribute(
        lambda a: choice(Inventory.objects.all()))
    name = factory.LazyFunction(fake.word)
    manufacturer = factory.LazyFunction(fake.company)
    notes = factory.LazyAttribute(lambda a: fake.sentence(nb_words=10))
    minQuantity = factory.LazyAttribute(
        lambda a: fake.random_int(min=0, max=10))


class ItemBatchFactory (factory.django.DjangoModelFactory):
    class Meta:
        model = ItemBatch
    item = factory.LazyAttribute(lambda a: choice(Item.objects.all()))
    expiryDate = factory.LazyFunction(fake.future_date)
    quantity = factory.LazyAttribute(
        lambda a: fake.random_int(min=10, max=20))
