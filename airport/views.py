from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
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
from airport.permissions import IsAdminOrReadOnly
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
    OrderListSerializer,
    OrderSerializer,
    RoleSerializer,
    RouteListSerializer,
    RouteRetrieveSerializer,
    RouteSerializer,
)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAdminOrReadOnly, )


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.select_related("role")
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CrewListSerializer
        return CrewSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAdminOrReadOnly, )


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        queryset = self.queryset.select_related("country")

        country = self.request.query_params.get("country")

        if country:
            country_id = int(country)
            queryset = queryset.filter(country__id=country_id)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirportListSerializer
        return AirportSerializer
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "country",
                type={"type": "number"},
                description="Filter by country id (example: ?country=1)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        
        if self.action == "retrieve":
            return RouteRetrieveSerializer
        
        return RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrReadOnly, )


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        queryset = self.queryset.all()

        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AirplaneListSerializer
        
        return AirplaneSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type={"type": "string"},
                description="Filter by name (example: ?name=boing)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrReadOnly, )

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


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).prefetch_related("tickets__flight__airplane")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return OrderListSerializer
        
        return OrderSerializer
    