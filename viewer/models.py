from django.db import models
from django.db.models import (
    DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField, DecimalField,
    Model, TextField, ImageField, BooleanField
)

# from django.contrib.auth.models import User

# Create your models here.


class Continent(Model):
    name = CharField(max_length=12)

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=30)
    continent = ForeignKey(Continent, on_delete=DO_NOTHING, default=None)

    def __str__(self):
        return f"{self.name} ({self.continent.name})"


class City(Model):
    name = CharField(max_length=30)
    country = ForeignKey(Country, on_delete=DO_NOTHING, default=None)

    def __str__(self):
        return f"{self.name} ({self.country.name})"

class Hotel(Model):
    name = CharField(max_length=30)
    standard = IntegerField(default=None, null=False)
    description = TextField(default=None)
    city = ForeignKey(City, on_delete=DO_NOTHING, default=None)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Airport(Model):
    name = CharField(max_length=50)
    city = ForeignKey(City, on_delete=DO_NOTHING, default=None)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Trip(Model):
    code = CharField(max_length=7)
    name = CharField(max_length=50)
    where_from = ForeignKey(Airport, on_delete=DO_NOTHING, related_name="where_from", default=None)
    where_to = ForeignKey(Airport, on_delete=DO_NOTHING, default=None)
    where_to_hotel = ForeignKey(Hotel, on_delete=DO_NOTHING, related_name="where_to", default=None)
    departure_date = DateField(default=None)
    return_date = DateField(default=None)
    duration = IntegerField(default=None, null=False)
    type = CharField(max_length=2)
    adult_price = DecimalField(max_digits=8, decimal_places=2)
    child_price = DecimalField(max_digits=8, decimal_places=2)
    promoted = BooleanField(default=False)
    adult_places = IntegerField(default=None, null=False)
    child_places = IntegerField(default=None, null=False)

