from django.urls import path
from .views import TicketListCreateView, TicketDetailView, DevSignupView

urlpatterns = [
    path("tickets", TicketListCreateView.as_view(), name="ticket-list-create"),
    path("tickets/<uuid:ticket_id>", TicketDetailView.as_view(), name="ticket-detail"),

    # Dev-only signup
    path("auth/dev-signup", DevSignupView.as_view(), name="dev-signup"),
]