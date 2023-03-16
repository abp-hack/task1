from random import choice
import string
from django.urls import path
import io
import pandas as pd
from django.db import models
from django.core.files import File
from reportlab.pdfgen import canvas
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib import admin
from django.template.response import TemplateResponse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect


# Пример аргумента fields
# {
#     'fieldNameInDjango':'FieldNameInExcel'
# }
def exportTXT(model, fields={}, filename='export.txt'):
        objects = list(model.objects.all())
        
        if len(fields) == 0:
            fields = {}
            for objField in model._meta.get_fields():
                if type(objField) ==  models.fields.reverse_related.ManyToOneRel: continue
                fields[objField.name] = objField.name

        data = {}

        for obj in objects:
            for field in obj._meta.get_fields():
                if type(field) ==  models.fields.reverse_related.ManyToOneRel: continue
                if fields[field.name] not in data.keys():
                    data[fields[field.name]] = [field.value_from_object(obj)]
                else:
                    data[fields[field.name]] += [field.value_from_object(obj)]
        
        dataFrame = pd.DataFrame(data)
        bytes = io.BytesIO()
        dataFrame.to_csv(bytes, header=None, index=None, sep=' ', mode='a')
        bytes.seek(0)
        return File(bytes, name=filename)



def exportExcel(model, fields={}, filename='export.xlsx'):
        objects = list(model.objects.all())
        
        if len(fields) == 0:
            fields = {}
            for objField in model._meta.get_fields():
                if type(objField) ==  models.fields.reverse_related.ManyToOneRel: continue
                fields[objField.name] = objField.name

        data = {}
        for obj in objects:
            for field in obj._meta.get_fields():
                if type(field) ==  models.fields.reverse_related.ManyToOneRel: continue
                if fields[field.name] not in data.keys():
                    data[fields[field.name]] = [field.value_from_object(obj)]
                else:
                    data[fields[field.name]] += [field.value_from_object(obj)]
        
        dataFrame = pd.DataFrame(data)

        bytes = io.BytesIO()
        dataFrame.to_excel(bytes, index=False)
        bytes.seek(0)
        return File(bytes, name=filename)

#ПРИМЕР ИСПОЛЬЗОВАНИЯ ЭКСОПРТА EXCEL
# def exportExcelLocal(self, request):
#         file = exportExcel(
#             model=self.model,
#             fields={
#                 'id':"АЙДИ",
#                 'balance':'БАЛАНС',
#                 'fullName':'ФИО',
#                 'service':'НОМЕР УСЛУГИ',
#                 'status':'СТАТУС',
#                 'validity':"ПЕРИОД ДЕЙСТВИЯ"
#             }
#         )     
#         return FileResponse(file.file, as_attachment=True, filename='file.xlsx')


class TableMixin(admin.ModelAdmin):
    change_list_template = 'tableMixin.html'
    def get_urls(self):
        urls = super().get_urls()

        myurls = [
            path('tableView/', self.admin_site.admin_view(self.table_view), name='table_view')
        ]
        return myurls + urls

    def table_data(self, request):
        return {
            "dataSource": [],
            "data": []
        }

    def table_view(self, request):
        context = dict(
               self.admin_site.each_context(request),
            )
        print(self.table_data(request))
        context.update(self.table_data(request))
        return TemplateResponse(request, 'tableTemplate.html', context)


#Надо обозначить в дочерним объекте либо X и Y, либо поля fX и fY
class ChartMixin(admin.ModelAdmin):
    X = []
    Y = []
    Type = "line"
    Label = 'Диграмма отчета'
    change_form_template ='chartTemplate.html'

    fX = []
    fY = []

    def getX(self):
        return self.X
    
    def getY(self):
        return self.Y
    

    def buildChart(self, x, y, type, label):
        self.X = self.buildX(x)
        self.Y = y
        self.Type = type
        self.Label = label


    def change_view(self, request, object_id, form_url='', extra_context=None):
        if self.fX != [] and len(self.X) == 0:
            for obj in self.fX.model.objects.all():
                self.X.append(self.fX.value_from_object(obj))
        if self.fY != [] and len(self.Y) == 0:
            for obj in self.fY.model.objects.all():
                self.Y.append(self.fY.value_from_object(obj))

        extra_context = extra_context or {}
        extra_context['x'] = self.getX()
        extra_context['y'] = self.getY()
        extra_context['type'] = self.Type
        extra_context['label'] = self.Label
        return super(ChartMixin, self).change_view(request, object_id, extra_context=extra_context)

#ПРИМЕР ИСПОЛЬЗОВАНИЯ ЧАРТОВ

# @admin.register(Service)
# class ServiceAdmin(ChartMixin):
#     # fX = Service._meta.get_field('name')
#     # fY = Service._meta.get_field('peoples')
#     X = [0,0, 1,2,3]
#     Y = [0,12, 2,3,10]
#     Type = 'bar'
#     list_display = ('name', 'region')
#     ordering = ('-name', )
#     list_filter = ('region', )



# Пример аргумента fields
# {
#     'FieldNameInExcel':'FieldNameInDjango'
# }


def importExcel(model, path, fields={}):
    if len(fields) == 0:
        fields = {}
        for objField in model._meta.get_fields():
            fields[objField.name] = objField.name
    
    dataFrame = pd.read_excel(path)
    dataFrame = dataFrame.to_dict('records') 


    for data in dataFrame:
        obj= model()
        for field in obj._meta.get_fields():
            if type(field) == models.fields.related.ForeignKey:
                for foreignObj in field.related_model.objects.all():
                    if str(foreignObj.id) == str(data[fields[field.name]]):
                        setattr(obj, field.name, foreignObj)
            elif type(field) == models.fields.reverse_related.ManyToOneRel:
                setattr(obj, field.name, None)
            else:
                setattr(obj, field.name, data[fields[field.name]])

        obj.save()

#ПРИМЕР ИСПОЛЬЗОВАНИЯ ИМПОРТА EXCEL

# def importExcelLocal(self, request):
#         if request.method == "POST":
#             excel_file = request.FILES["excel_file"]
#             importExcel(
#                 model=self.model,
#                 path=excel_file,
#                 fields={
#                 'id':"АЙДИ",
#                 'balance':'БАЛАНС',
#                 'fullName':'ФИО',
#                 'service':'НОМЕР УСЛУГИ',
#                 'status':'СТАТУС',
#                 'validity':"ПЕРИОД ДЕЙСТВИЯ"
#             }   
#             )
#             self.message_user(request, "EXCEL файл был импортирован")
#             return redirect("..")

#       form = ExcelImportForm()
#         payload = {"form": form}
#         return render(
#             request,   "excel_form.html", payload
#         )


def createPDF(template_path=None, texts=[  {'text': "HelloWorld!", 'cords': (0,0)} ], images=[], filename='exportPDF.pdf', font_size=14):

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        pdfmetrics.registerFont(TTFont('FreeSans', 'touragency/templates/Font.ttf'))
        can.setFont('FreeSans', font_size)

        for image in images:
            can.drawImage(image['path'], image['cords'][0], image['cords'][1], width=None, height=None)

        for text in texts:
            try:
                can.drawString(text['cords'][0], text['cords'][1], text['text'])
            except: print('Неправильный формат надписи')
        
        can.save()  
        packet.seek(0)  


        if template_path == None:
            return File(packet, name=filename)
        else:
            new_pdf = PdfReader(packet)

            existing_pdf = PdfReader(open(template_path, "rb"))
            output = PdfWriter()
            
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

            response_bytes_stream = io.BytesIO()
            output.write(response_bytes_stream)
            response_bytes_stream.seek(0)  


            return File(response_bytes_stream, name=filename)

'''
 ПРИМЕР ИСПОЛЬЗОВАНИЯ CREATEPDF

 def exportPDF(self, request):
    qr = qrcode.make(str(self.data.id))
    qr.save('touragency/templates/a.png')
    pdf = createPDF(
        texts=[
            {'text':"Уникальный код: " + str(self.data.id), 'cords':(100, 140)},
            {'text':"Услуга: " + str(self.data.service), 'cords':(100, 160)},
            {'text':"Cрок действия: " + str(self.data.validity), 'cords':(100, 180)},
            {'text':"Владелец: " + str(self.data.fullName), 'cords':(100, 200)},
            {'text':"баланc: " + str(self.data.balance), 'cords':(100, 220)},
            {'text':"Поздравляем с покупкой сертификата!", 'cords':(100, 240)},
        ],
        images=[
            {
                'path': 'touragency/templates/a.png',
                'cords': (200,250)
            }
        ]
    )
    return FileResponse(pdf.file, as_attachment=True, filename='attempt1.pdf', content_type='application/pdf')
'''



def sendEmail(subject, message, recipients, files=[]):
    mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipients)
    
    if len(files) > 0:
        for f in files:
            mail.attach(f.name, f.read(), 'pdf/plain')
    
    mail.send()


#ПРИМЕР ИСПОЛЬЗОВАНИЯ ОТПРАВКИ СООБЩЕНИЯ СО ВЛОЖЕНИЕМ
# def sendCertificate(self, request):
#     file = createPDF(texts=[
#         {'text': str(self.data.id), 'cords': (200,750)},
#         {'text': str(self.data.service), 'cords': (100,710)},
#         {'text': str(self.data.fullName), 'cords': (100,710)},
#     ])
#     sendEmail('Тест моего почтового сервера', str(self.data), ['firesieht@mail.ru'], [file])
#     return HttpResponseRedirect('../')



def generate_password():
    return ''.join([choice(string.ascii_letters) for _ in range(6)])






class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()



class ImportExportMixin(admin.ModelAdmin):
    change_list_template = 'changeListImportExport.html'

    fields_manager = {}

    def get_urls(self):
        urls = super().get_urls()

        self.nameImportUrl = 'importExcel/'
        self.nameExportUrl = 'exportExcel/'
        self.nameExportTXTUrl = 'exportTXT/'
        murls = [
            path('exportExcel/', self.exportExelFunc),
            path('importExcel/', self.importExelFunc),
            path('exportTXT/', self.exportTXTFunc),

        ]
        return murls+urls 

   
    def exportExelFunc(self, request):
        file = exportExcel(self.model, fields=self.fields_manager)
        self.message_user(request, 'ФАЙЛ ЭКСПОРТИРОВАН')
        return FileResponse(file.file, as_attachment=True, filename=file.name)
    def exportTXTFunc(self, request):
        file = exportTXT(self.model, fields=self.fields_manager)
        self.message_user(request, 'ФАЙЛ ЭКСПОРТИРОВАН')
        return FileResponse(file.file, as_attachment=True, filename=file.name)

    def importExelFunc(self, request):
        if request.method == 'POST':
            file = request.FILES['excel_file']
            importExcel(self.model, path=file, fields=self.fields_manager)
            self.message_user(request, 'ФАЙЛ ЗАГРУЖЕН')
            return redirect("..")
        form = ExcelImportForm()
        payload = {'form':form}
        return render(request, "excel_form.html", payload)


    def changelist_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        extra_context['nameImportUrl'] = self.nameImportUrl
        extra_context['nameExportUrl'] = self.nameExportUrl
        extra_context['nameExportTXTUrl'] = self.nameExportTXTUrl

        return super(ImportExportMixin, self).changelist_view(request, extra_context=extra_context)