from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction

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


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_row(
            attrs["row"],
            attrs["flight"].airplane.rows,
            serializers.ValidationError
        )
        Ticket.validate_seat(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            serializers.ValidationError
        )

        return data

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "flight"]
        validators = [UniqueTogetherValidator(
            queryset=Ticket.objects.all(), fields=["row", "seat", "flight"]
            )
        ]


class TicketSeatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["row", "seat"]       


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crews"]


class FlightInfoSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(many=False, read_only=True, slug_field="route_name")
    airplane = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")

    class Meta:
        model = Flight
        fields = ["route", "airplane", "departure_time", "arrival_time"]


class FlightRetrieveSerializer(serializers.ModelSerializer):
    route = RouteListSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=True)
    crews = CrewListSerializer(many=True, read_only=True)
    taken_seats = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crews", "taken_seats"]


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.SlugRelatedField(many=False, read_only=True, slug_field="route_name")
    airplane = serializers.SlugRelatedField(many=False, read_only=True, slug_field="name")
    crews = serializers.StringRelatedField(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = ["id", "route", "airplane", "departure_time", "arrival_time", "crews", "tickets_available"]


class TicketInfoSerializer(TicketSerializer):
    flight = FlightInfoSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketInfoSerializer(many=True, read_only=True)
