#from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets, status
from .models import Products, Photo, Notification 
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProductsSerializers, PhotoSerializers, NotificationSerializers
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


'''API для уведомлений с возможностью фильтрации'''
class NotificationViewSet(viewsets.ModelViewSet):
    queryset=Notification.objects.all()
    serializer_class=NotificationSerializers #акой сериализатор 
    # permission_classes = [permissions.IsAuthenticated]  # позже 
    
    def get_queryset(self):
        # Можно фильтровать по прочитанным/непрочитанным через параметры запроса
            queryset = super().get_queryset()
            is_read = self.request.query_params.get('is_read')
            if is_read is not None:
                if is_read.lower() == 'true':
                    queryset = queryset.filter(is_read=True)
                elif is_read.lower() == 'false':
                    queryset = queryset.filter(is_read=False)
            return queryset
    
