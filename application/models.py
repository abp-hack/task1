from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save


class Student(models.Model):
    SEX_CHOICES = (
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский')
    )
    
    name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    mindame = models.CharField(max_length=100, verbose_name='Отчество')
    gender = models.CharField(choices=SEX_CHOICES, verbose_name='Пол', max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100, verbose_name='Пароль')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



class SumModel(models.Model):
    email = models.CharField(max_length=100)
    sum = models.IntegerField()


class Sums(models.Model):
    field_a = models.IntegerField()
    field_b = models.IntegerField()
    model = models.ForeignKey(SumModel, on_delete=models.CASCADE)


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'

class Hotel(models.Model):
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'
    
    name = models.CharField('Имя', max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, verbose_name='Регион')


    def __str__(self):
        return f'Отель {self.name}'


class Status(models.Model):
    text = models.CharField(max_length=100, verbose_name='Текст')
    
    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class HotelNumber(models.Model):
    CAT_CHOICES = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )

    hotel = models.ForeignKey(Hotel, related_name='numbers', verbose_name='Отель', on_delete=models.CASCADE)
    number = models.CharField('Номер', max_length=10)
    status = models.ForeignKey(Status, related_name='numbers', verbose_name='Статус', on_delete=models.CASCADE)
    category = models.CharField('Категория', choices=CAT_CHOICES, default='Стандарт', max_length=100)
    how_many = models.IntegerField('Количество мест', default=2)
    date_started = models.DateField('Дата заезда', null=True, blank=True)
    date_end = models.DateField('Дата выезда', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Номер отеля'
        verbose_name_plural = 'Номера отелей'
    
    def __str__(self):
        from booking.models import Booking
        suf = ''
        if self.status.text == 'Занят':
            print(self.date_started)
            if self.date_started and self.date_end:
                suf += f'{self.date_started.strftime("%m.%d.%Y")}-{self.date_end.strftime("%m.%d.%Y")}'
                # book = Booking.objects.filter(number=self).first().payer
                # suf += book.payer
        return f'Номер {self.number}; {suf}'

    def clean(self):
        if self.date_started and not self.date_end:
            raise ValidationError('Укажите дату выезда')
        if self.date_end and not self.date_started:
            raise ValidationError('Укажите дату заезда')
        if self.date_started and self.date_started:
            now = datetime.datetime.now().date()
            if self.date_started >= self.date_end:
                raise ValidationError('Дата выезда не может быть раньше или равна дате заезда')
            if self.date_started <= now and self.date_end > now:
                self.status = Status.objects.get(text='Занят')
        if self.category == 'Стандарт' or self.category == 'Люкс':
            if self.how_many > 2:
                raise ValidationError(f'В номерах типа {self.category} не может быть больше 2 человек')
        else:
            if self.how_many > 4:
                raise ValidationError(f'В номерах типа {self.category} не может быть больше 4 человек')


class Report(models.Model):
    date = models.DateField('Дата на которую надо формировать отчет')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name='Отель')

    # @property
    # def numbers(self): 
    #     return list(sorted(
    #         self.rooms, key=lambda x: x.status.text
    #     ))

    # def clean(self):
    #     rrs = []
    #     for room in HotelNumber.objects.filter(hotel=self.hotel):
    #         rr = RoomReport(category=room.category, number=room.number, report=self)
    #         if self.date >= room.date_started and self.date < room.date_end:
    #             rr.status = Status.objects.get(text='Занят')
    #         else:
    #             rr.status = Status.objects.get(text='Свободен (чистый)')
    #         rrs.append(rr)
    #     for rr in sorted(rrs, key=lambda x: x.status.text):
    #         rr.save()
    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
    
    def __str__(self):
        return f'Отчет об отеле: {self.hotel} на дату: {self.date.strftime("%m.%d.%Y")}; Стандартных номеров - {len(self.rooms.filter(category="Стандарт", status__text="Свободен (чистый)"))}; Номеров люкс - {len(self.rooms.filter(category="Люкс", status__text="Свободен (чистый)"))}; Апартаментов - {len(self.rooms.filter(category="Апартамент", status__text="Свободен (чистый)"))} '


class RoomReport(models.Model):
    CAT_CHOICES = (
        ('Стандарт', 'Стандарт'),
        ('Люкс', 'Люкс'),
        ('Апартамент', 'Апартамент')
    )
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='rooms')
    category = models.CharField('Категория', choices=CAT_CHOICES, default='Стандарт', max_length=100)
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.CASCADE)
    number = models.CharField('Номер', max_length=10)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        from booking.models import Booking
        suf = ''
        if self.status.text == 'Занят':
            print(self.date_started)
            if self.date_started and self.date_end:
                suf += f'{self.date_started.strftime("%m.%d.%Y")}-{self.date_end.strftime("%m.%d.%Y")}'
                # book = Booking.objects.filter(number=self).first().payer
                # suf += book.payer
        return f'Номер {self.number}; {suf}'

@receiver(post_save, sender=Report)
def generate_report(sender, instance, **kwargs):
    rrs = []
    for room in HotelNumber.objects.filter(hotel=instance.hotel):
        rr = RoomReport(category=room.category, number=room.number, report=instance)
        if room.date_started and room.date_end:
            if instance.date >= room.date_started and instance.date < room.date_end:
                rr.status = Status.objects.get(text='Занят')
            else:
                rr.status = Status.objects.get(text='Свободен (чистый)')
        else:
            rr.status = Status.objects.get(text='Свободен (чистый)')
        rrs.append(rr)
    for rr in sorted(rrs, key=lambda x: x.category):
        rr.save()