from django.contrib import admin
from viewer.models import City, Hotel, Airport, Trip  # Country, Continent,

# Register your models here.
# admin.site.register(Continent)
# admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Airport)
admin.site.register(Trip)
