from django.db import models
from django_countries.fields import CountryField
from django.db.models import (
    DO_NOTHING, CharField, DateField, DateTimeField, ForeignKey, IntegerField, DecimalField,
    Model, TextField, ImageField, BooleanField, Choices
)
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MinValueValidator

# from django.contrib.auth.models import User

# Create your models here.


class City(Model):

    AF = 'Africa'
    AN = 'Antarctica'
    AS = 'Asia'
    EU = 'Europe'
    NA = 'North America'
    OC = 'Australia & Oceania'
    SA = 'South America'

    CONTINENT_CHOICES = (
        (None, 'select continent'),
        (AF, 'Africa'),
        (AN, 'Antarctica'),
        (AS, 'Asia'),
        (EU, 'Europe'),
        (NA, 'North America'),
        (OC, 'Australia & Oceania'),
        (SA, 'South America')
    )

    name = CharField(max_length=30)
    country = CountryField(blank_label="select country")
    continent = CharField(max_length=30, choices=CONTINENT_CHOICES, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country.name}, {self.continent})"


class Hotel(Model):
    name = CharField(max_length=100)
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
    BB = 'BB'
    HB = 'HB'
    FB = 'FB'
    AI = 'AI'

    TYPE_CHOICES = (
        (None, 'select type of stay'),
        (BB, 'bed & breakfast'),
        (HB, 'half board'),
        (FB, 'full board'),
        (AI, 'all inclusive'),
    )

    code = CharField(max_length=7)
    where_from = ForeignKey(City, on_delete=DO_NOTHING, related_name="where_from", default=None)
    airport_depart = ChainedForeignKey(
        Airport,
        chained_field="where_from",
        chained_model_field="city",
        related_name="airport_depart",
        show_all=False,
        auto_choose=True,
        sort=True)
    where_to = ForeignKey(City, on_delete=DO_NOTHING,  related_name="where_to", default=None)
    airport_arrive = ChainedForeignKey(
        Airport,
        chained_field="where_to",
        chained_model_field="city",
        related_name="airport_arrive",
        show_all=False,
        auto_choose=True,
        sort=True)
    where_to_hotel = ChainedForeignKey(
        Hotel,
        chained_field="where_to",
        chained_model_field="city",
        show_all=False,
        auto_choose=True,
        sort=True)
    departure_date = DateField(default=None)
    return_date = DateField(default=None)
    duration = IntegerField(default=None, null=False, validators=[MinValueValidator(1)])
    type = CharField(max_length=20, choices=TYPE_CHOICES, blank=False)
    adult_price = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    child_price = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    promoted = BooleanField(default=False)
    adult_places = IntegerField(default=None, null=False, validators=[MinValueValidator(0)])
    child_places = IntegerField(default=None, null=False, validators=[MinValueValidator(0)])
    description = TextField(default=None)
    short_description = TextField(default=None)
    image = ImageField(upload_to="images", default=None, null=True)
    image_small = ImageField(upload_to="images", default=None, null=True)



