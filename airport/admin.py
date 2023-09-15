from django.contrib import admin

from airport.models import (
    Airplane,
    AirplaneType,
    Airport,
    Country,
    Crew,
    Flight,
    Order,
    Role,
    Route,
    Ticket,
)


admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Airport)
admin.site.register(Country)
admin.site.register(Crew)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Role)
admin.site.register(Route)
admin.site.register(Ticket)
