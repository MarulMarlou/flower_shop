from django.contrib import admin
from .models import Client, Flower, Order, OrderItem, Ticket

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'segment']

@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'status', 'created_at']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'flower', 'quantity']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'subject', 'created_at', 'is_resolved']