from rest_framework import serializers
from .models import Product, Category, Comment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'category', 'price', 'stock', 'view_count', 'like_count', 'image', 'slug']
        read_only_fields = ['id', 'like_count', 'view_count']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"




