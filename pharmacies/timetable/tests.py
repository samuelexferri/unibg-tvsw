from django.test import TestCase

from shop.models import *
from timetable.views import *


# CASO IN CIO SIANO MENO DI 42
class AlgoritmoCalculateTimetable1(TestCase):
    def test_algorithm_calculate1(self):
        user1 = User.objects.create(username='Testuser1')
        user2 = User.objects.create(username='Testuser2')
        user3 = User.objects.create(username='Testuser3')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")

        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=5, location="Bergamo", description="Text")
        farmacia1.save()
        farmacia2.save()
        farmacia3.save()
        algorithm_timetable(self)

        count = Timetable.objects.all().count()

        self.assertEqual(count, 42)


# CASO IN CUI SONO PIU DI 42
class AlgoritmoCalculateTimetable2(TestCase):
    def test_algorithm_calculate1(self):
        user1 = User.objects.create(username='Testuser1')
        user2 = User.objects.create(username='Testuser2')
        user3 = User.objects.create(username='Testuser3')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=20, location="Bergamo", description="Text")

        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=25, location="Bergamo", description="Text")

        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=35, location="Bergamo", description="Text")
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
class AlgoritmoCalculateTimetable1(TestCase):
    def test_algorithm_calculate1(self):
        user1 = User.objects.create(username='Testuser1')
        user2 = User.objects.create(username='Testuser2')
        user3 = User.objects.create(username='Testuser3')

        farmacia1 = Pharmacy.objects.create(owner=user1, name="farmacia1", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=15, location="Bergamo", description="Text")

        farmacia2 = Pharmacy.objects.create(owner=user2, name="farmacia2", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=10, location="Bergamo", description="Text")

        farmacia3 = Pharmacy.objects.create(owner=user3, name="farmacia3", image="farmacia.png", x=50, y=50,
                                            slot4hMinWeek=17, location="Bergamo", description="Text")
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
