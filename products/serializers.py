from rest_framework import serializers
from .models import Products, Photo, Notification 
class ProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model= Products
        fields= ['id', 'name', 'article', 'quantity', 'location', 'created_at']#все поля модели, позже прописать 
#сириализатор для фотофиксации 
class PhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'product', 'image', 'uploaded_at', 'description']
        read_only_fields = ['uploaded_at'] 

class NotificationSerializers(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.name', read_only=True, default='')
    class Meta:
        model=Notification
        fields = ['id', 'text', 'is_read', 'created_at', 'product', 'product_name']
        read_only_fields = ['created_at']