from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product, Like, Comment
from .serializers import ProductSerializer, CommentSerializer, CategorySerializer
from django.db.models import Q
from users.permissions import *
from rest_framework.generics import get_object_or_404


class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)


class ProductListView(APIView):
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        category = request.query_params.get('category')
        if category:
            products = Product.objects.filter(category=category)
            
        search = request.query_params.get("search")
        if search:
            products = Product.objects.filter(
                Q(title__icontains=search) | Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )[start:end]
        else:
            products = Product.objects.all()[start:end]
        serializer = ProductSerializer(products, many=True)
        return Response({
            "msg" : "Products list",
            "products" : serializer.data
        })



class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated, CanProductUpdate]
    def patch(self, request, id):
        product = get_object_or_404(Product, id=id)
        self.check_object_permissions(request, product)
        serializer = ProductSerializer(data=request.data, instance=product, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)



class ProductDeleteView(APIView):
    permission_classes = [IsAuthenticated, CanProductUpdate]
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        self.check_object_permissions(request, product)
        product.delete()
        return Response({"message": "Product deleted "}, status=204)



class ProductDetailView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.view_count += 1
        product.save()
        serializer = ProductSerializer(product)
        return Response({
            "msg" : "Product detail",
            "data" : serializer.data,
            "comments_count" : product.comments.count()
        })



class LikedView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        product = get_object_or_404(Product, id=id) 
        like, created = Like.objects.get_or_create(
            author=request.user,
            product=product
            )        
        if not created:
            product.like_count -= 1
            like.delete()
            product.save()
            return Response({"msg" : "Unliked"})
        product.like_count += 1
        product.save()
        return Response({"msg" : "Liked"})



class CommentsView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = Comment.objects.filter(product=product)
        return Response({
            "msg" : "Product comments",
            "data" : CommentSerializer(comments, many=True).data
        })

    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product,author=request.user)
        return Response(serializer.data, status=201)


class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated, CanProductUpdate]
    def delete(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response({
            "msg" : "Comment deleted"
        })





class CategoriesView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)




class UserLikesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.filter(likes__author=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response({
            "msg" : "Siz like bosgan mahsulotlar",
            "data" : serializer.data
        })

class UserCommentsView(APIView):
    def get(self, request):
        products = Product.objects.filter(comments__author=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response({
            "msg" : "Siz comment yozgan mahsulotlar",
            "data" : serializer.data
        })







