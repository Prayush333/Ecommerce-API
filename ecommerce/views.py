from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response(OrderSerializer(orders, many=True).data)

    @action(detail=False, methods=['post'])
    def place_order(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "Cart is empty."}, status=400)

       
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"detail": f"Not enough stock for {item.product.name}"},
                    status=400
                )

        
        order = Order.objects.create(user=user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.stock -= item.quantity
            item.product.save()
            item.delete()

        return Response({"detail": "Order placed successfully."}, status=201)

