from rest_framework import serializers
from .models import Products, Photo 
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
