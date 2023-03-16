from django.contrib import admin
from .models import Booking
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Client, Guest, Payment
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from application.models import HotelNumber, Status
from django.shortcuts import redirect
from django.db.models import Q


class GuestTabular(admin.TabularInline):
    model = Guest
    extra = 0


@admin.register(Guest)
class GuestAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    mask = {
         'tel': '+7(900)000-00-00'
        }
    exclude = ('book', )
    class Media:
        js = ['https://unpkg.com/imask@6.4.2/dist/imask.js', 'tel_mask.js']
admin.site.register(Client)          
# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Booking
#     fields = ('date_started', 'date_end', 'date_len', 'hotel')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    class Meta:
        model = Payment
    
    def response_change(self, request, obj):
        hotel_number = obj.booking.number
        hotel_number.status = Status.objects.get(text='Занят')
        hotel_number.date_started = obj.booking.date_started
        hotel_number.date_end = obj.booking.date_end
        hotel_number.save()
        return super(PaymentAdmin, self).response_change(request, obj)


@admin.register(Booking)
class BookingAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
    class Meta:
        model = Booking
    fields = ('date_started', 'date_end', 'hotel', 'number', 'cost', 'payer', 'checked')
    dynamic_fields = ('number', )
    inlines = (GuestTabular, )
    
    
    class Media:
        js = ['https://unpkg.com/imask@6.4.2/dist/imask.js', 'tel_mask.js']
    
    
    def response_change(self, request, obj):
        if obj.checked:
            p = Payment.objects.create(booking=obj, cost=obj.cost)
            return redirect(f'/admin/booking/payment/{p.id}/change/')
        return super(BookingAdmin, self).response_change(request, obj)


    def response_add(self, request, obj):
        if obj.checked:
            p = Payment.objects.create(booking=obj, cost=obj.cost)
            return redirect(f'/admin/booking/payment/{p.id}/change/')
        return super(BookingAdmin, self).response_change(request, obj)


    def get_dynamic_number_field(self, data):
        q = HotelNumber.objects.filter(Q(
            status__text='Свободен (чистый)'
    ) | Q(status__text='Свободен (грязный)'))
        if 'hotel' in data.keys():
            q = q.filter(hotel=data['hotel'])
        return q, data['number'], False
