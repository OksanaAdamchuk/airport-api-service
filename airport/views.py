from django.shortcuts import render
from rest_framework import viewsets

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
from airport.serializers import (
    AirplaneSerializer,
    AirplaneTypeSerializer,
    AirportListSerializer,
    AirportSerializer,
    CountrySerializer,
    CrewListSerializer,
    CrewSerializer,
    FlightSerializer,
    OrderSerializer,
    RoleSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    RouteSerializer,
    TicketSerializer,
)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.select_related("role")
    serializer_class = CrewSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CrewListSerializer
        return CrewSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.select_related("country")
    serializer_class = AirportSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirportListSerializer
        return AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        
        return RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

