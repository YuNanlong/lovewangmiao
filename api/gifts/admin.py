from django.contrib import admin
from api.gifts.models import Ticket

# Register your models here.

class TicketAdmin(admin.ModelAdmin):
    model = Ticket

admin.site.register(Ticket, TicketAdmin)
