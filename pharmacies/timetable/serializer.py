from rest_framework import serializers

from shop.serializer import PharmacySerializer
from timetable.models import Timetable


class TimetableSerializer(serializers.ModelSerializer):
    pharmacy = PharmacySerializer(read_only=True)

    class Meta:
        model = Timetable
        fields = "__all__"
