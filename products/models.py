from django.db import models
import qrcode #создает объект изображения в памяти
from io import BytesIO #буфер 
from django.core.files import File # для сохранения файла 
from PIL import Image 
import os 
class Products (models.Model): 
    name= models.CharField(max_length=200, verbose_name= 'Название товара') #verbose_name- удобночитаемое имя  
    article= models.CharField(max_length=50, verbose_name= 'Артикул', unique= True)
    quantity= models.IntegerField(default= 0, verbose_name= 'Количество на складе' )
# Create your models here.
    location= models.CharField(null=True,  blank= True, max_length=100, verbose_name='Место хранения (стеллаж/ячейка)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    qr_code=models.ImageField(upload_to='qrs/', blank=True, null=True, verbose_name='QR-код') #upload_to- куда сохранить кркод ...sklad/media/qrs/ 
    def __str__(self):
        return f'{self.name},({self.article})'
    #При создании нового товара, нужно автоматически сгенерировать для него кркод и закрепить за ID товар
    # ID появляется только в момент сохранения. 
    # ТОвар будет сохраняться 2  раза : первый для получения ID
    def save(self, *arg, **kwargs): #*args позиционные, **kwargs именованные 
        if not self.pk: #если нет первичного ключа? сохранить товар и присвоить ID  
            super().save(*arg, **kwargs)
    #создание кр кода 
        if not self.qr_code:
            qr=qrcode.QRCode(
                version=1, #самый маленький размер QR-кода (21x21 пикселей)
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10, # каждый "квадратик" QR будет размером 10 пикселей.
                border=4
            )
            qr.add_data(str(self.id))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            image_name = f'qr_{self.id}.png'   # имя файла

            # Сохраняем файл в поле qr_code
            self.qr_code.save(image_name, File(buffer), save=False)
            buffer.close()

        # Сохраняем объект с обновлённым qr_code
        super().save(*arg, **kwargs)
    class Meta:
        verbose_name='Товар'
        verbose_name_plural='Товары'
#класс "Фото" для фотофисации товаров на разных этапах 
class Photo(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='photos', verbose_name='Товар')
    image=models.ImageField(upload_to='product_photos/', verbose_name="Фотография")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки') #время фотофиксаци  
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Описание (опционально)') #комментарий к фото 
    def __str__(self):
        return f'Фото товара {self.product.name} от {self.uploaded_at.strftime("%d.%m.%Y")}'
    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'
        ordering = ['-uploaded_at']   # сначала новые фотофиксации 
