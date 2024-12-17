from django.contrib import admin
from viewer.models import Country, Hotel, Airport, Trip  # Continent,

# Register your models here.
# admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Hotel)
admin.site.register(Airport)
admin.site.register(Trip)
