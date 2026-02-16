"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

from .views import (
    HealthView,
    PublicTokenObtainPairView,
    PublicTokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Core API (기본: 인증 필요)
    path("api/", include("tickets.urls")),

    # Core API (기본: 인증 필요)
    path("api/", include("tickets.urls")),

    # Public endpoints
    path("api/health/", HealthView.as_view(), name="health"),

    # Auth (Public)
    path("api/auth/token/", PublicTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),

    # OpenAPI schema + Swagger UI (Public)
    path("api/schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny]), name="swagger-ui"),

]
