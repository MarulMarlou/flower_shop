# Create your models here.
from django.db import models

class Client(models.Model):
    SEGMENT_CHOICES = [
        ('regular', 'Постоянный клиент'),
        ('one_time', 'Одноразовый'),
        ('corporate', 'Корпоративный'),
    ]
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Эл. почта", unique=True)
    phone = models.CharField("Телефон", max_length=20)
    segment = models.CharField(  # Новое поле
        "Сегмент",
        max_length=20,
        choices=SEGMENT_CHOICES,
        default='one_time'
    )
    created_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Flower(models.Model):
    """Цветок"""
    id = models.AutoField(primary_key=True)  # Явное определение id
    name = models.CharField("Название", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Остаток на складе")

    def __str__(self):
        return self.name

class Order(models.Model):
    """Заказ"""
    id = models.AutoField(primary_key=True)  # Явное определение id
    STATUS_CHOICES = [
        ('received', 'Принят'),
        ('in_progress', 'В сборке'),
        ('delivered', 'Доставлен'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    flowers = models.ManyToManyField(Flower, through='OrderItem')
    address = models.TextField("Адрес доставки")
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default='received'
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id}"

class OrderItem(models.Model):
    """Элемент заказа"""
    id = models.AutoField(primary_key=True)  # Явное определение id
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.IntegerField("Количество", default=1)

    class Meta:
        unique_together = [['order', 'flower']]

class Ticket(models.Model):
    """Обращение клиента"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    subject = models.CharField("Тема", max_length=200)
    message = models.TextField("Сообщение")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_resolved = models.BooleanField("Решено", default=False)

    def __str__(self):
        return f"{self.subject} (ID: {self.id})"