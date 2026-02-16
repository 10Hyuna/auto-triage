from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Ticket
from .serializers import TicketCreateSerializer, TicketSerializer, DevSignupSerializer

from drf_spectacular.utils import extend_schema
from config.api_schemas import ErrorResponseSerializer

from django.conf import settings

from django.shortcuts import get_object_or_404


"""
    POST /api/tickets
    - (source, external_id) unique로 중복 유입 방지
    - 이미 있으면 200 + existing 리턴
    - 새로 생성되면 201 리턴
"""
class TicketListCreateView(APIView):

    @extend_schema(
        tags=["Tickets"],
        summary="티켓 목록 조회",
        responses={200: TicketSerializer(many=True), 401: ErrorResponseSerializer},
    )
    def get(self, request):
        qs = Ticket.objects.all().order_by("-created_at")[:100]
        return Response(TicketSerializer(qs, many=True).data)


    @extend_schema(
        tags=["Tickets"],
        summary="티켓 생성 (idempotent)",
        description="(source, external_id) 기준으로 중복 유입을 방지합니다. 이미 존재하면 200을 반환합니다.",
        request=TicketCreateSerializer,
        responses={
            200: TicketSerializer,
            201: TicketSerializer,
            400: ErrorResponseSerializer,
            401: ErrorResponseSerializer,
        },
    )
    def post(self, request):
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        source = data["source"]
        external_id = data["external_id"]

        # 이미 존재하면 그대로 반환 
        existing = Ticket.objects.filter(source=source, external_id=external_id).first()
        if existing:
            return Response(TicketSerializer(existing).data, status=status.HTTP_200_OK)

        # 없으면 생성 (동시성 경쟁 시 IntegrityError 처리)
        try:
            with transaction.atomic():
                ticket = Ticket.objects.create(**data)
        except IntegrityError:
            ticket = Ticket.objects.get(source=source, external_id=external_id)
            return Response(TicketSerializer(ticket).data, status=status.HTTP_200_OK)

        return Response(TicketSerializer(ticket).data, status=status.HTTP_201_CREATED)


class TicketDetailView(APIView):
    @extend_schema(
        tags=["Tickets"],
        summary="티켓 상세 조회",
        responses={200: TicketSerializer, 404: ErrorResponseSerializer, 401: ErrorResponseSerializer},
    )
    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        return Response(TicketSerializer(ticket).data)
    
class DevSignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=["Auth"],
        summary="개발용 회원가입",
        description="개발 환경에서만 사용합니다. ALLOW_DEV_SIGNUP=true일 때만 동작합니다.",
        auth=[],
        request=DevSignupSerializer,
        responses={201: dict, 400: ErrorResponseSerializer, 403: ErrorResponseSerializer},
    )
    def post(self, request):
        if not getattr(settings, "ALLOW_DEV_SIGNUP", False):
            return Response(
                {"code": "forbidden", "message": "회원가입이 비활성화되어 있습니다.", "details": {}},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = DevSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)