from rest_framework import serializers
from .models import Ticket

from django.contrib.auth.models import User

class DevSignupSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용 중인 username 입니다.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("source", "external_id", "title", "body")
        validators = []

    def validate(self, attrs):
        body = (attrs.get("body") or "").strip()
        if len(body) < 5:
            raise serializers.ValidationError({"body": "본문이 너무 짧습니다."})
        if len(body) > 20000:
            raise serializers.ValidationError({"body": "본문이 너무 깁니다."})
        attrs["body"] = body

        title = (attrs.get("title") or "").strip()
        attrs["title"] = title[:255]
        return attrs
    
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "source", "external_id", "title", "body", "status", "created_at", "updated_at")
        read_only_fields = fields