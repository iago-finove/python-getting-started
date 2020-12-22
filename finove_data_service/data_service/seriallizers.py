from rest_framework import serializers
from . import models


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)


class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ResponseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResponseRecord

        fields = (
            "id",
            "source",
            "source_url",
            "data",
            "verification",
            "created_at",
            "updated_at",
            "cnpj",
        )
