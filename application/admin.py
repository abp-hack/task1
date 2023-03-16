from django.contrib import admin
#from .models import DynamicModel, DynamicModelSummarization
from django.contrib.auth.forms import AuthenticationForm
#from .models import Station, StationManager, Product, Student

from dynamic_admin_forms.admin import DynamicModelAdminMixin
from django.contrib.admin.sites import AdminSite
from django.shortcuts import redirect
from django.db.models import Q
from .utils import ImportExportMixin
from dynamic_admin_forms.admin import DynamicModelAdminMixin
from django import forms
from admincharts.admin import AdminChartMixin
from .models import Student, SumModel, Sums

from django.contrib.admin.sites import AdminSite
from .models import Hotel, HotelNumber, Status, Region, RoomReport, Report

#admin.site.register(Status)
admin.site.register(Region)

class RoomReportTabular(admin.TabularInline):
    model = RoomReport
    extra = 0


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    class Meta:
        model = Report
    inlines = (RoomReportTabular, )


class HotelNumberTabular(admin.TabularInline):
    model = HotelNumber
    extra = 0


# @admin.register(HotelNumber)
# class HotelNumberAdmin(admin.ModelAdmin):
#     class Meta:
#         model = HotelNumber
#     list_display = ('hotel', 'number', 'status')


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = (HotelNumberTabular, )
    class Meta:
        model = Hotel
    
    class Media:
        js = ['dates_display.js']

# another_site = AdminSite(name='another_admin')

# class RegisterAdmin(admin.ModelAdmin):
#     class Meta:
#         model = Student

# another_site.register(Student, RegisterAdmin)

# @admin.register(Student)
# class MyModelAdmin(AdminChartMixin, admin.ModelAdmin):
#     list_chart_type = "bar"
#     list_chart_options = {"aspectRatio": 6}
#     list_chart_config = None

#     def get_list_chart_data(self, queryset):
#         return {
#             "labels": ["a", "b"],
#             "datasets": [
#                 {
#                     "label": "a",
#                     "data": [1, 2],
#                     "backgroundColor": "#79aec8"
#                 }
#             ]
#         }


# class SumsInline(admin.TabularInline):
#     #exclude = ('model',)
#     model = Sums

# @admin.register(SumModel)
# class SumModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
#     inlines = (SumsInline, )
#     tabular_fields = ('field_a', 'field_b')
#     dynamic_tabular_fields = ('field_a', 'field_b')
#     fields = ('sum', 'email')
#     dynamic_fields = ('sum', )
#     parent_name = 'sums_set'
#     mask = {
#         'email': '0000-00'
#     }
    
#     def get_dynamic_field_a_field(self, data):
#         print(data)
#         return  data['field_a'], False
    
#     def get_dynamic_field_b_field(self, data):
#         print(data)
#         return int(data['field_a']) * 10, False
    
#     def get_dynamic_sum_field(self, data):
#         print(data)
#         return [], sum(map(lambda x: int(x['field_a']) * 10, data['dynamic_fields'])), False
#     class Meta:
#         model = SumModel

# @admin.register(Student)
# class StudentAdmin(ImportExportMixin, admin.ModelAdmin):
#     Type = 'bar'
#     class Meta:
#         model = Student
    
#     def getX(self):
#         return [1, 2, 5, 6]
#     def getY(self):
#         return [1, 4, 2, 7]
    
#     def response_add(self, request, obj, *args):
#         return redirect('')


# @admin.register(Product)
# class ProductAdmin(TableMixin, admin.ModelAdmin):
#     class Meta:
#         model = Product
    
#     def table_data(self, request):
#         return {
#             "dataSource":[ {
#                 "key": '1',
#                 "name": 'Mike',
#                 "age": "32",
#                 "address": '10 Downing Street',
#                 'fixed': 'left'
#                 },
#                 {
#                 "key": '2',
#                 "name": 'John',
#                 "age": 42,
#                 "address": '10 Downing Street',
#                 }],
#             "data": [
#                 {
#                     "title": 'Name',
#                     "dataIndex": 'name',
#                     "key": 'name',
#                 },
#                 {
#                     "title": 'Age',
#                     "dataIndex": 'age',
#                     "key": 'age',
#                 },
#                 {
#                     "title": 'Address',
#                     "dataIndex": 'address',
#                     "key": 'address',
#                 },
#             ]
#         }



# class AuthForm(AuthenticationForm):
#     password_again = forms.CharField(
#         label="Password again",
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "current-password"})
#     )


# # class Site(AdminSite):
# #     login_form = AuthForm


# class ProductAdminManager(admin.TabularInline):
#     model = Product
#     fields = ('name', 'station')
#     extra = 0

#     def formfield_for_foreignkey(self, db_field, request=None, **kwargs):

#         field = super(ProductAdminManager, self).formfield_for_foreignkey(db_field, request, **kwargs)

#         if db_field.name == 'station':
#             field.queryset = field.queryset.filter(~Q(state='Демонтаж'))

#         return field

# class ProductAdmin(admin.TabularInline):
#     model = Product
#     fields = ('name', 'price')
#     extra = 0

    

# @admin.register(Product)
# class StationManagerAdmin(ChartMixin, admin.ModelAdmin):
#     X = [1, 2, 3]
#     Y = [2, 3, 4]

#     class Meta:
#         model = Product
#         fields = ('name', 'station')


# admin_site = Site(name='myadmin')



# class FieldInlineTabular(admin.TabularInline):
#     pass
# #         model = StationManager
# #         fields = ('name', 'station')

# class FieldInlineTabular(DynamicModelAdminMixin, admin.TabularInline):
#     model = DynamicModelSummarization
#     fields = ('field_a', 'field_b', 'summarization')
#     dynamic_fields = ('summarization', )

#     def get_formset(self, request, *args, **kwargs):
#         return super().get_formset(request, *args, **kwargs)

#     def get_dynamic_summarization_field(self, data):
#         s = 0
#         try:
#             s += data['field_a']
#         except: pass
#         try:
#             s += data['field_b']
#         except: pass

#         return [], s, False


# @admin.register(DynamicModel)
# class DinamicModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
#     inlines = [FieldInlineTabular, ]

#     tabular_fields = ['field_a', 'field_b']
#     dynamic_tabular_fields = ['field_b', 'field_a']
#     dynamic_fields = ['summarization']
#     parent_name = 'child'
#     mask = {
#         "name" : "+{7}(000)000-00-00"
#     }

#     def get_dynamic_field_b_field(self, data):
#         return int(data['field_a']) * 10, False

# # @admin.register(DynamicModel)
# # class DinamicModelAdmin(DynamicModelAdminMixin, admin.ModelAdmin):
# #     inlines = [FieldInlineTabular, ]

# #     tabular_fields = ['field_a', 'field_b']
# #     dynamic_tabular_fields = ['field_b', 'field_a']
# #     dynamic_fields = ['summarization']
# #     parent_name = 'child'
# #     mask = {
# #         "name" : "+{7}(000)000-00-00"
# #     }

# #     def get_dynamic_field_b_field(self, data):
# #         return int(data['field_a']) * 10, False    
#     def get_dynamic_field_a_field(self, data):
#         return int(data['field_a']), False
    
#     def get_dynamic_summarization_field(self, data):
#         sum(map(lambda x: int(x['field_a']) * 10, data['dynamic_fields']))
#         return [], sum(map(lambda x: int(x['field_a']) * 10, data['dynamic_fields'])), False