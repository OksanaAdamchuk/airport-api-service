from types import NoneType
from typing import Iterable, Optional
from django.db import models
from django.conf import settings
from django.forms import ValidationError


class Role(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="crews")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["role", "last_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.role})"


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="airports"
    )

    class Meta:
        ordering = ["-country", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.country})"


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="source_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="destination_routes"
    )
    distance = models.IntegerField()

    @property
    def route_name(self) -> str:
        return f"{self.source}-{self.destination}"

    class Meta:
        ordering = ["source", "destination"]

    def __str__(self) -> str:
        return self.route_name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="flights")
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crews = models.ManyToManyField(Crew, related_name="flights", blank=True)

    class Meta:
        ordering = ["departure_time", "route"]

    def __str__(self) -> str:
        return f"{self.route.route_name} at {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    @staticmethod
    def validate_seat(seat: int, num_seats: int, error_to_raise):
        if not (1 <= seat <= num_seats):
            raise error_to_raise(
                {"seat": ("seat must be in range " f"[1, {num_seats}], not {seat}")}
            )

    @staticmethod
    def validate_row(row: int, num_rows: int, error_to_raise):
        if not (1 <= row <= num_rows):
            raise error_to_raise(
                {"row": ("row must be in range " f"[1, {num_rows}], not {row}")}
            )

    def clean(self) -> None:
        Ticket.validate_row(self.row, self.flight.airplane.rows, ValidationError)
        Ticket.validate_seat(
            self.seat, self.flight.airplane.seats_in_row, ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )
