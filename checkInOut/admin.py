from django.contrib import admin
from .models import CheckIn, CheckOut, TodayNumbers, TodayLogoutNumbers, EmptyModel
from application.models import HotelNumber
import datetime
from booking.models import Booking
from .models import CheckIn, CheckOut, CheckGuest
from application.models import HotelNumber, Status

from booking.models import Client, Guest, Payment
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from django.db.models import Q
from django.shortcuts import redirect
from .models import CheckGuest
# admin.site.register(CheckOut)
# admin.site.register(CheckIn)

@admin.action(description='Оформить заезд')
def get_check_in(modeladmin, request, queryset):
    book = queryset.first()
    check = CheckIn.objects.create(
        date_start=datetime.datetime.now(),
        date_end=book.date_end,
        hotel=book.hotel,
        booking=book,
        number=book.number
    )
    return redirect(f'/admin/checkInOut/checkin/{check.id}/change/')


@admin.action(description='Оформить выезд')
def get_check_out(modeladmin, request, queryset):
    check_out = CheckOut.objects.create(date=datetime.datetime.now().date(), number=queryset.first().number, hotel=queryset.first().hotel)
    return redirect(f'/admin/checkInOut/checkout/{check_out.id}/change/')


@admin.register(TodayNumbers)
class EmptyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Booking.objects.filter(date_started=datetime.datetime.now().date())
    actions = [get_check_in]
    class Meta:
        model = TodayNumbers


@admin.register(TodayLogoutNumbers)
class EmptyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Booking.objects.filter(date_end=datetime.datetime.now().date())
    actions = [get_check_out]
    class Meta:
        model = TodayLogoutNumbers

@admin.register(EmptyModel)
class EmptyModelAdmin(admin.ModelAdmin):
    change_list_template = 'screen.html'
    class Meta:
        model = EmptyModel




admin.site.register(Status)
class GuestStacked(admin.StackedInline):
    model = CheckGuest
    fields = ('guest',)
    extra = 0

@admin.register(CheckIn)
class CheckInAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = CheckIn
    fields = ('date_start', 'hotel', 'booking', 'number', 'date_end')
    dynamic_fields = ('number', )
    inlines = (GuestStacked, )

    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.filter(Q(
            status__text='Свободен (чистый)'
    ) | Q(status__text='Свободен (грязный)'))
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return q, data['number'], False

@admin.register(CheckOut)
class CheckOutAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = CheckOut

    fields = ('date', 'hotel', 'number')
    dynamic_fields = ('number', )
    inlines = (GuestStacked, )


    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.filter(Q(
            status__text='Занят'
    ) | Q(status__text='Заняты (грязный)'))
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return q, data['number'], False
