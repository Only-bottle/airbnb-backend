from rest_framework.test import APITestCase

from . import models


class TestAmenities(APITestCase):
    NAME = "Amenity Test"
    DESC = "Amenity Des"

    def setUp(self):  # 다른 모든 테스트들이 실행되기 전에 수행됨
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):
        response = self.client.get("/api/v1/rooms/amenities/")
        data = response.json()
        print(data)

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )
