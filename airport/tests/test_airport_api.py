from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Airplane, AirplaneType, Airport, Country
from airport.serializers import AirplaneListSerializer, AirportListSerializer


AIRPORTS_URL = reverse("airport:airport-list")

class PublicAirportApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.country1 = Country.objects.create(name="Ukraine")
        self.country2 = Country.objects.create(name="Poland")
        self.airport1 = Airport.objects.create(
            name="Test Ukrainian Airport",
            closest_big_city="Kyiv",
            country=self.country1
        )
        self.airport2 = Airport.objects.create(
            name="Test Polish Airport",
            closest_big_city="Krakow",
            country=self.country2
        )
        self.airport3 = Airport.objects.create(
            name="New Polish Airport",
            closest_big_city="Warsaw",
            country=self.country2
        )

    def test_list_airports(self) -> None:
        res = self.client.get(AIRPORTS_URL)
        airports = Airport.objects.all()
        serializer = AirportListSerializer(airports, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_airports_by_country_id(self) -> None:
        res = self.client.get(AIRPORTS_URL, {"country": f"{self.country2.id}"})

        serializer1 = AirportListSerializer(self.airport1)
        serializer2 = AirportListSerializer(self.airport2)
        serializer3 = AirportListSerializer(self.airport3)

        self.assertNotIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertIn(serializer3.data, res.data["results"])

    def test_retrieve_airport_detail(self) -> None:
        url = reverse("airport:airport-detail", args=[self.airport1.id])
        res = self.client.get(url)

        serializer = AirportListSerializer(self.airport1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_create_airport_not_allowed(self) -> None:
        data = {
            "name": "Ukrainian Airport",
            "closest_big_city": "Lviv",
            "country": self.country1
        }
        res = self.client.post(AIRPORTS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_airport_not_allowed(self) -> None:
        url = reverse("airport:airport-detail", args=[self.airport1.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAirportApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "Testpassword123@"
        )
        self.client.force_authenticate(self.user)

        self.country1 = Country.objects.create(name="Ukraine")
        self.airport1 = Airport.objects.create(
            name="Test Ukrainian Airport",
            closest_big_city="Kyiv",
            country=self.country1
        )

    def test_create_airport_not_allowed(self) -> None:
        data = {
            "name": "Ukrainian Airport",
            "closest_big_city": "Lviv",
            "country": self.country1.id
        }
        res = self.client.post(AIRPORTS_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airport_not_allowed(self) -> None:
        url = reverse("airport:airport-detail", args=[self.airport1.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

class AdminUserAirportApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "Testpassword123@", is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.country1 = Country.objects.create(name="Ukraine")
        self.airport1 = Airport.objects.create(
            name="Test Ukrainian Airport",
            closest_big_city="Kyiv",
            country=self.country1
        )

    def test_create_airport(self) -> None:
        payload = {
            "name": "Ukrainian Airport",
            "closest_big_city": "Lviv",
            "country": self.country1.id
        }
        res = self.client.post(AIRPORTS_URL, payload)
        airport = Airport.objects.get(pk=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            if key == "country":
                self.assertEqual(payload[key], airport.country.id)
            else:
                self.assertEqual(payload[key], getattr(airport, key))

    def test_update_airport(self) -> None:
        payload = {
            "name": "Next Airport",
            "closest_big_city": "Lviv",
            "country": self.country1.id
        }
        url = reverse("airport:airport-detail", args=[self.airport1.id])
        res = self.client.patch(url, payload)
        airport = Airport.objects.get(pk=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in payload:
            if key == "country":
                self.assertEqual(payload[key], airport.country.id)
            else:
                self.assertEqual(payload[key], getattr(airport, key))

    def test_delete_airport(self) -> None:
        url = reverse("airport:airport-detail", args=[self.airport1.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
