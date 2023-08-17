from rest_framework import serializers

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
    Ticket
)


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ["id", "name"]


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ["id", "first_name", "last_name", "role"]


class CrewListSerializer(serializers.ModelSerializer):
    role = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    
    class Meta:
        model = Crew
        fields = ["id", "full_name", "role"]


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ["id", "name"]


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = ["id", "name", "closest_big_city", "country"]


class AirportListSerializer(AirportSerializer):
    country = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ["id", "source", "destination", "distance"]

class RouteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ["id", "route_name", "distance"]


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportListSerializer(many=False, read_only=True)
    destination = AirportListSerializer(many=False, read_only=True)


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ["id", "name"]


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = ["id", "name", "rows", "seats_in_row", "airplane_type", "capacity"]

class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crews"]


class FlightRetrieveSerializer(FlightSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)
    crews = CrewListSerializer(many=True, read_only=True)


class FlightListSerializer(FlightSerializer):
    route = serializers.SlugRelatedField(many=False, read_only=True, slug_field="route_name")
    airplane = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    crews = serializers.StringRelatedField(many=True)


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "created_at", "user"]


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight", "order"]
