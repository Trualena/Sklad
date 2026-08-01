#from django.shortcuts import render

from rest_framework import viewsets, status
from .models import Products, Photo 
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductsSerializers, PhotoSerializers
class ProductViewSet(viewsets.ModelViewSet):
    queryset= Products.objects.all()
    serializer_class=ProductsSerializers#для преобразования данных из python в json и обратно

    @action(detail=True, methods=['post'], url_path='upload-photo')
    def upload_photo(self, request, pk=None):
        """Загружает фото для конкретного товара (pk = id товара)"""
        product = self.get_object()   # получаем товар по id из URL

        # Проверяем, есть ли файл в запросе
        if 'image' not in request.FILES:
            return Response({'error': 'Файл не передан'}, status=status.HTTP_400_BAD_REQUEST)

        # Создаём запись в БД
        photo = Photo.objects.create(
            product=product,
            image=request.FILES['image'],
            description=request.data.get('description', '')  # если передали описание
        )

        # Сериализуем созданный объект и возвращаем
        serializer = PhotoSerializers(photo)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    