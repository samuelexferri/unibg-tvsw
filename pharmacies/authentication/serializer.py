from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)  # Hide in GET
    password = serializers.CharField(write_only=True)  # Hide in GET

    class Meta:
        model = User
        fields = "__all__"
