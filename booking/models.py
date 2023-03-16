from django.db import models
from application.models import HotelNumber, Hotel
from django.db.models import Q
from django.core.exceptions import ValidationError
import datetime

class Guest(models.Model):
    class Meta():
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'
    fullName = models.CharField(max_length=150, verbose_name='ФИО')
    tel = models.CharField(verbose_name='Телефон', max_length=100)
    book = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, related_name='clients')
   

    def __str__(self):
        return f'Гость {self.fullName}, Тел:{self.tel}'

class Client(models.Model):
    payer = models.CharField(max_length=150, verbose_name='Плательщик')
    choices = [
        ('Физ. лицо','Физ. лицо'),
        ('Юр. лицо','Юр. лицо'),
    ]
    type_of_payer = models.CharField(max_length=50, choices=choices, verbose_name='Вид плательщика')

    def __str__(self):
        return f'Плательщик {self.type_of_payer} {self.payer}'
    class Meta():
        verbose_name='Плательщик'
        verbose_name_plural = 'Плательщики'


class Booking(models.Model):
    date_started = models.DateField('Дата начала', null=True, blank=True)
    date_end = models.DateField('Дата окончания', null=True, blank=True)
    date_len = models.PositiveIntegerField('Сколько ночей', blank=True, null=True)
    number = models.ForeignKey(HotelNumber, verbose_name='Номер отеля', on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель', null=True)
    date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата заезда')
    cost = models.DecimalField('Стоимость', default=0, decimal_places=2, max_digits=32)
    payer = models.ForeignKey(Client, verbose_name='Плательщик', on_delete=models.CASCADE, null=True)
    checked = models.BooleanField('Бронь подтверждена', default=False)
    
    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'

    def clean(self):
        if self.date_end is None and self.date_len is None:
            raise ValidationError("Укажите конечную дату")
        if self.date_end is not None:
            self.date_len = (self.date_end - self.date_started).days
        if self.date_len:
            self.date_end = self.date_started + datetime.timedelta(days=self.date_len)
        if self.date_end <= self.date_started:
            raise ValidationError('Дата конца не может быть меньше даты начала')
        numbers = HotelNumber.objects.filter(hotel=self.hotel)

        bookings = Booking.objects.filter(
            (
                Q(date_started__lte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__gte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__gte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__gte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__lte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__lte=self.date_end) &
                Q(date_started__lt=self.date_end)
            ) | (
                Q(date_started__gte=self.date_started) &
                Q(date_end__gt=self.date_started) &
                Q(date_end__lte=self.date_end) &
                Q(date_started__lt=self.date_end)
            )
        )
        bookings = list(filter(lambda x: x.id != self.id, bookings))
        #raise ValidationError(f'На такие даты уже есть номера {", ".join(map(str, bookings))}')
        booked_numbers = list(map(lambda x: x.number, bookings))
        num = None
        for number in numbers:
            if number not in booked_numbers:
                num = number
                break
        if not num:
            raise ValidationError(f'На такие даты свободных номеров не найдено')
        else:
            self.number = num
    
    def __str__(self):
        return f'{self.date_started.strftime("%m.%d.%Y")} - {self.date_end.strftime("%m.%d.%Y")}; {"Потдвтерждено" if self.checked else "Не подтвреждено"}'


class Payment(models.Model):
    class Meta():
        verbose_name='Оплата'
        verbose_name_plural = 'Оплаты'
    
    booking = models.ForeignKey(Booking, verbose_name='Основание (бронирование)', on_delete=models.CASCADE)
    cost = models.DecimalField(decimal_places=2, max_digits=32)

    def __str__(self) -> str:
        return f'Подтверждение {self.booking}, на сумму {self.cost}'
    
    def save(self, *args, **kwargs):
        #Здесь напиши на сохранение платежа: Подставление Дат заезда и выезда + статус номера на занят
        super(Payment, self).save(*args, **kwargs)