from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    AirplaneViewSet,
    AirportViewSet,
    CountryViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
    RoleViewSet,
    RouteViewSet,
    TicketViewSet,
)


router = routers.DefaultRouter()
router.register("roles", RoleViewSet)
router.register("crews", CrewViewSet)
router.register("countries", CountryViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = router.urls

app_name = "airport"
