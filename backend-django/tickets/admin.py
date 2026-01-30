from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "source", "status", "created_at")
    list_filter = ("status", "source")
    search_fields = ("external_id", "title", "body")
