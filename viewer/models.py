from django.db import models

from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

from django_countries.fields import CountryField
from smart_selects.db_fields import ChainedForeignKey

from django.db.models import (
    DO_NOTHING, CharField, DateField, ForeignKey, IntegerField, DecimalField, Model, TextField, ImageField,
    BooleanField, EmailField
)


class City(Model):

    # These constants contain continents
    AF = 'Africa'
    AN = 'Antarctica'
    AS = 'Asia'
    EU = 'Europe'
    NA = 'North America'
    OC = 'Australia & Oceania'
    SA = 'South America'

    # This dictionary contains choices for the continent field
    CONTINENT_CHOICES = {
        None: 'select continent',
        AF: 'Africa',
        AN: 'Antarctica',
        AS: 'Asia',
        EU: 'Europe',
        NA: 'North America',
        OC: 'Australia & Oceania',
        SA: 'South America',
    }

    name = CharField(max_length=30)
    # The CountryField is a special Django field which contains choices of countries from all over the world
    country = CountryField(blank_label="select country")
    continent = CharField(max_length=30, choices=CONTINENT_CHOICES, blank=True)

    def __str__(self):
        return f"{self.name} ({self.country.name}, {self.continent})"


class Hotel(Model):
    name = CharField(max_length=100)
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
    # These constants contain the abbreviations for hotel service standards
    BB = 'BB'
    HB = 'HB'
    FB = 'FB'
    AI = 'AI'

    # This dictionary contains choices for hotel service standards
    STANDARD_CHOICES = {
        None: 'select service standard',
        BB: 'bed & breakfast',
        HB: 'half board',
        FB: 'full board',
        AI: 'all inclusive',
        }

    code_regex = RegexValidator(regex=r'^[A-Za-z]{4}\d{3}',  # This is the validator for the code format
                                message="The code must correspond to the above described format.")
    code = CharField(max_length=7,  validators=[code_regex])
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
    service_standard = CharField(max_length=20, choices=STANDARD_CHOICES, blank=False)
    adult_price = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    child_price = DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    promoted = BooleanField(default=False)
    adult_places = IntegerField(default=None, null=False, validators=[MinValueValidator(0)])
    child_places = IntegerField(default=None, null=False, validators=[MinValueValidator(0)])
    description = TextField(default=None)
    short_description = TextField(default=None)
    image = ImageField(upload_to="images", default=None, null=True, blank=True)
    image_small = ImageField(upload_to="images", default=None, null=True, blank=True)


class PurchasedTrip(Model):
    trip = ForeignKey(Trip, on_delete=DO_NOTHING, default=None)
    firstname = CharField(max_length=128, null=False)
    lastname = CharField(max_length=128, null=False)
    birth_date = DateField(default=None, null=False)
    email = EmailField(max_length=70, blank=False, default=None, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',  # This is the validator for the phone number format
                                 message="Phone number must be entered in the format:"
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    amount_adult = IntegerField(default=None, null=False)
    amount_child = IntegerField(default=None, null=False)
    total_price = DecimalField(max_digits=8, decimal_places=2, default=None, null=False)



