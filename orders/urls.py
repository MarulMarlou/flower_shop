from django.urls import path, include
from .views import client_list, create_ticket, analytics, send_to_delivery, create_order, order_list, ticket_list, \
    update_order_status, client_detail, update_client, confirm_delivery, create_client
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, FlowerViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'flowers', FlowerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('clients/', client_list, name='client_list'),
    path('support/', create_ticket, name='create_ticket'),
    path('analytics/', analytics, name='analytics'),
    path('orders/<int:order_id>/send-to-delivery/', send_to_delivery, name='send_to_delivery'),
    path('create-order/', create_order, name='create_order'),
    path('orders/', order_list, name='order_list'),
    path('tickets/', ticket_list, name='ticket_list'),
    path('orders/<int:order_id>/update-status/', update_order_status, name='update_order_status'),
    path('clients/<int:client_id>/', client_detail, name='client_detail'),
    path('clients/<int:client_id>/update/', update_client, name='update_client'),
    path('orders/<int:order_id>/confirm-delivery/', confirm_delivery, name='confirm_delivery'),
    path('support/create/', create_ticket, name='create_ticket'),
    path('clients/create/', create_client, name='create_client'),
    path('', include(router.urls)),
]