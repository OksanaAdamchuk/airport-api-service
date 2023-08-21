from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter

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
    AirplaneListSerializer,
    AirplaneSerializer,
    AirplaneTypeSerializer,
    AirportListSerializer,
    AirportSerializer,
    CountrySerializer,
    CrewListSerializer,
    CrewSerializer,
    FlightListSerializer,
    FlightRetrieveSerializer,
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

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        
        return AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related("crews")

        route = self.request.query_params.get("route")

        if route:
            route_id = int(route)
            queryset = queryset.filter(route__id=route_id)

        if self.action == "list":
            queryset = (
                queryset.
                annotate(
                    tickets_available=(
                        (F("airplane__rows") * F("airplane__seats_in_row")) - Count("tickets")
                    )
                )
            )

        return queryset
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "route",
                type={"type": "number"},
                description="Filter by route id (example: ?route=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightRetrieveSerializer
        if self.action == "list":
            return FlightListSerializer
        
        return FlightSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
