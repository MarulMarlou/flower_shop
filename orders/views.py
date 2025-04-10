import base64
from django.utils import timezone
from io import BytesIO
from rest_framework import viewsets
from .models import Client, Flower, Order, OrderItem
from .serializers import ClientSerializer, FlowerSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render, redirect
from .models import Client, Ticket
from django.db.models import Count
from django.http import JsonResponse
import matplotlib.pyplot as plt

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'orders/client_list.html', {'client_list': clients})

def create_ticket(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        # Пример: связать с текущим клиентом (для теста)
        client = Client.objects.first()  # Замените на текущего пользователя
        Ticket.objects.create(client=client, subject=subject, message=message)
        return redirect('client_list')
    return render(request, 'orders/support_form.html')

def analytics(request):
    popular_flowers = Flower.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]

    segments = Client.objects.values('segment').annotate(count=Count('id')).order_by('-count')

    orders_by_month = Order.objects.extra({
        'month': "MONTH(created_at)"
    }).values('month').annotate(total=Count('id')).order_by('month')
    fig, ax = plt.subplots()
    ax.bar(
        [flower.name for flower in popular_flowers],
        [flower.order_count for flower in popular_flowers]
    )
    ax.set_title('Популярные цветы')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return render(request, 'orders/analytics.html', {
        'popular_flowers': popular_flowers,
        'segments': segments,
        'orders_by_month': orders_by_month,
        'image_base64': image_base64,
    })

def send_to_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    # Пример интеграции (заменится на реальный API)
    delivery_response = {
        "status": "success",
        "message": f"Заказ {order_id} отправлен в службу доставки."
    }
    return JsonResponse(delivery_response)


def create_order(request):
    if request.method == 'POST':
        client_id = request.POST['client_id']
        flower_id = request.POST['flower_id']
        quantity = int(request.POST['quantity'])

        client = Client.objects.get(id=client_id)
        flower = Flower.objects.get(id=flower_id)

        if flower.stock >= quantity:
            flower.stock -= quantity
            flower.save()

            order = Order.objects.create(
                client=client,
                address=request.POST.get('address', 'Не указано'),
                status='received'
            )
            OrderItem.objects.create(
                order=order,
                flower=flower,
                quantity=quantity
            )
            return redirect('order_list')
        else:
            error_message = f"Недостаточно {flower.name} на складе. Доступно: {flower.stock}"
            return render(request, 'orders/create_order.html', {
                'error': error_message,
                'clients': Client.objects.all(),
                'flowers': Flower.objects.all()
            })

    return render(request, 'orders/create_order.html', {
        'clients': Client.objects.all(),
        'flowers': Flower.objects.all()
    })


def order_list(request):
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = Order.objects.filter(status=status_filter)
    else:
        orders = Order.objects.all()

    return render(request, 'orders/order_list.html', {
        'order_list': orders,
        'status_filter': status_filter
    })

def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'orders/ticket_list.html', {'tickets': tickets})

def update_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        new_status = request.POST['status']
        order.status = new_status
        order.save()
        return redirect('order_list')
    return render(request, 'orders/update_order_status.html', {'order': order})

def client_detail(request, client_id):
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client=client)
    return render(request, 'orders/client_detail.html', {
        'client': client,
        'orders': orders
    })

def update_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client.first_name = request.POST['first_name']
        client.last_name = request.POST['last_name']
        client.phone = request.POST['phone']
        client.segment = request.POST['segment']
        client.save()
        return redirect('client_list')
    return render(request, 'orders/update_client.html', {'client': client})

def confirm_delivery(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'delivered'
    order.delivery_date = timezone.now()  # Используйте timezone.now()
    order.save()
    return redirect('order_list')

def create_ticket(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        client = Client.objects.get(id=request.POST['client_id'])
        Ticket.objects.create(client=client, subject=subject, message=message)
        return redirect('ticket_list')
    return render(request, 'orders/create_ticket.html', {
        'clients': Client.objects.all()
    })


def create_client(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        segment = request.POST['segment']

        Client.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            segment=segment
        )
        return redirect('client_list')

    return render(request, 'orders/create_client.html')