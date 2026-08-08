from django.contrib import admin
from .models import Products, Photo, History 
'''admin.site.register(Products)
admin.site.register(Photo)'''

''' класс для отображения и редактирования истории на главной странице '''
class Historyinline(admin.TabularInline): #тип встраиваемого отображения в виде таблицы. Альтернатива StackedInline (каждая запись в отдельном блоке)
    model=History
    extra=0# 0 пустых строк для добавления новых записей показывать, потому что история создаётся по форме 
    readonly_fields = ['action_type', 'created_at', 'details', 'user'] #поля которые нельзя редактировать
    can_delete = False #нельзя удалить запись 
    fields=['action_type', 'created_at', 'details', 'user'] #поля и их порядок 
    ordering=['-created_at']
    '''связывание моделей и их настроек для админки с помощью декоратора "@" '''
@admin.register(Products)#регистрация класса в админке вместо admin.site.register()
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'article', 'quantity', 'location', 'created_at']
    inlines = [Historyinline]#добавление историяя в карточку редактирования товара 
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'uploaded_at', 'image']
    readonly_fields = ['uploaded_at']#поле даты нельзя редактироват ь
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'action_type', 'created_at', 'details']
    list_filter = ['action_type', 'created_at']#фильтры 
    search_fields = ['product__name', 'details']#поиск по названию 
    readonly_fields = ['product', 'action_type', 'created_at', 'details']#только для чтения 