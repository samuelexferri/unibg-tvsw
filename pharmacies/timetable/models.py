from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shop.models import Pharmacy
from timetable import choices


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)

    day = models.CharField(max_length=250, choices=choices.day_choices, blank=True)
    slot4h = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(6)])
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Timetable " + self.id.__str__() + " - " + self.pharmacy.__str__() + " - " + self.day.__str__() + " S" + self.slot4h.__str__()

    class Meta:
        verbose_name_plural = "Timetables"
