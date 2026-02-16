from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

class PublicTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Auth"], summary="토큰 발급 (로그인)")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(tags=["Auth"], summary="토큰 갱신")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HealthView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=["Health"], summary="헬스체크", auth=[],responses={200: dict})
    def get(self, request):
        return Response({"status": "ok"})