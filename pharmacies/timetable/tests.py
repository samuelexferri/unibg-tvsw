from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Pharmacy
from timetable.models import Timetable
from timetable.views import algorithm_timetable

"""
View tests
"""


class ViewTest(TestCase):
    def test_homepage(self):
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_view(self):
        url = reverse("timetable:view_timetable")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_calculate(self):
        url = reverse("timetable:calc_timetable")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)


# CASO IN CUI SIANO MENO DI 42
class AlgoritmoCalculateTimetable1(TestCase):
    def test_algorithm_calculate1(self):
        user1 = User.objects.create(username="Testuser1")
        user2 = User.objects.create(username="Testuser2")
        user3 = User.objects.create(username="Testuser3")

        farmacia1 = Pharmacy.objects.create(
            owner=user1,
            name="farmacia1",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )

        farmacia2 = Pharmacy.objects.create(
            owner=user2,
            name="farmacia2",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )

        farmacia3 = Pharmacy.objects.create(
            owner=user3,
            name="farmacia3",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=5,
            location="Bergamo",
            description="Text",
        )
        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        algorithm_timetable(self)

        count = Timetable.objects.all().count()
        self.assertEqual(count, 42)


# CASO IN CUI SONO PIU DI 42
class AlgoritmoCalculateTimetable2(TestCase):
    def test_algorithm_calculate2(self):
        user1 = User.objects.create(username="Testuser1")
        user2 = User.objects.create(username="Testuser2")
        user3 = User.objects.create(username="Testuser3")

        farmacia1 = Pharmacy.objects.create(
            owner=user1,
            name="farmacia1",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=20,
            location="Bergamo",
            description="Text",
        )

        farmacia2 = Pharmacy.objects.create(
            owner=user2,
            name="farmacia2",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=25,
            location="Bergamo",
            description="Text",
        )

        farmacia3 = Pharmacy.objects.create(
            owner=user3,
            name="farmacia3",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=35,
            location="Bergamo",
            description="Text",
        )
        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        algorithm_timetable(self)

        c1 = Timetable.objects.filter(pharmacy=farmacia1).count()
        c2 = Timetable.objects.filter(pharmacy=farmacia2).count()
        c3 = Timetable.objects.filter(pharmacy=farmacia3).count()

        count = Timetable.objects.all().count()
        self.assertEqual(count, 80)
        self.assertEqual(c1, 20)
        self.assertEqual(c2, 25)
        self.assertEqual(c3, 35)


# CASO IN CUI SONO 42
class AlgoritmoCalculateTimetable3(TestCase):
    def test_algorithm_calculate3(self):
        user1 = User.objects.create(username="Testuser1")
        user2 = User.objects.create(username="Testuser2")
        user3 = User.objects.create(username="Testuser3")

        farmacia1 = Pharmacy.objects.create(
            owner=user1,
            name="farmacia1",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=15,
            location="Bergamo",
            description="Text",
        )

        farmacia2 = Pharmacy.objects.create(
            owner=user2,
            name="farmacia2",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=10,
            location="Bergamo",
            description="Text",
        )

        farmacia3 = Pharmacy.objects.create(
            owner=user3,
            name="farmacia3",
            image="farmacia.png",
            x=50,
            y=50,
            slot4hMinWeek=17,
            location="Bergamo",
            description="Text",
        )
        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        algorithm_timetable(self)

        c1 = Timetable.objects.filter(pharmacy=farmacia1).count()
        c2 = Timetable.objects.filter(pharmacy=farmacia2).count()
        c3 = Timetable.objects.filter(pharmacy=farmacia3).count()

        count = Timetable.objects.all().count()
        self.assertEqual(c1, 15)
        self.assertEqual(c2, 10)
        self.assertEqual(c3, 17)

        self.assertEqual(count, 42)
