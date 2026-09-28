from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db import transaction
from users.permissions import *
from .models import Cart, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer



class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = Cart.objects.filter(owner=request.user)
        serializer = CartSerializer(items, many=True)
        total = sum(item.total_price for item in items)
        return Response({
            "msg" : "Savatcha",
            "data" : serializer.data,
            "total_price" : total
        })

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)

        item, created = Cart.objects.get_or_create(
            owner=request.user,
            product=product,
            defaults={'quantity': 0}
        )
        if item.quantity + quantity > product.stock:
            if created:
                item.delete()
            return Response({"msg" : "Omborda yetarli mahsulot yo'q"}, status=400)

        item.quantity += quantity
        item.save()
        return Response(CartSerializer(item).data, status=201)

    def delete(self, request):
        Cart.objects.filter(owner=request.user).delete()
        return Response({"msg" : "Savatcha tozalandi"})



class CartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        item = get_object_or_404(Cart, pk=pk, owner=request.user)
        quantity = int(request.data.get('quantity', item.quantity))
        if quantity < 1:
            return Response({"msg" : "Miqdor kamida 1 bo'lishi kerak"}, status=400)
        if quantity > item.product.stock:
            return Response({"msg" : "Omborda yetarli mahsulot yo'q"}, status=400)
        item.quantity = quantity
        item.save()
        return Response(CartSerializer(item).data)

    def delete(self, request, pk):
        item = get_object_or_404(Cart, pk=pk, owner=request.user)
        item.delete()
        return Response({"msg" : "Mahsulot savatchadan o'chirildi"})



class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(owner=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response({
            "msg" : "Buyurtmalaringiz",
            "data" : serializer.data
        })

    def post(self, request):
        cart_items = Cart.objects.filter(owner=request.user)
        if not cart_items.exists():
            return Response(
                {"msg": "Savatcha bo'sh"},
                status=400
            )
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(owner=request.user)

        total = 0
        for item in cart_items:
            product = item.product
            if item.quantity > product.stock:
                return Response(
                    {"msg": f"{product.title} omborda yetarli emas"},
                    status=400
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )
            product.stock -= item.quantity
            product.save()

            total += item.total_price
        order.total_price = total
        order.save()
        cart_items.delete()
        return Response(OrderSerializer(order).data,status=201)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, owner=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)



class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, owner=request.user)
        if order.status != 'pending':
            return Response({"msg": "Bu buyurtmani bekor qilib bo'lmaydi"},status=400)

        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        order.status = 'cancelled'
        order.save()

        return Response({"msg": "Buyurtma bekor qilindi"})