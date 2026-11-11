from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import User, GroceryItem, Order, OrderItem
from .serializers import (
    UserRegistrationSerializer, GroceryItemSerializer,
    OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminOrStaff, IsAdminUserOnly


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class GroceryItemListCreateView(generics.ListCreateAPIView):
    queryset = GroceryItem.objects.all().order_by('-id')
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name', 'brand', 'category']


class GroceryItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroceryItem.objects.all()
    serializer_class = GroceryItemSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUserOnly]


class UserOrderHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=OrderCreateSerializer, responses={201: OrderSerializer})
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        items_data = validated_data.get('items', [])
        if not items_data:
            return Response({"error": "No items provided in order."}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = 0
        prepared_items = []

        for item_data in items_data:
            try:
                g_item = GroceryItem.objects.get(id=item_data['item_id'])
            except GroceryItem.DoesNotExist:
                return Response({"error": f"Item with id {item_data['item_id']} not found."}, status=status.HTTP_404_NOT_FOUND)

            qty = item_data['quantity']
            if g_item.stock_quantity < qty:
                return Response({"error": f"Insufficient stock for '{g_item.name}' (Available: {g_item.stock_quantity})."}, status=status.HTTP_400_BAD_REQUEST)

            discount_price = g_item.price * (1 - (g_item.discount / 100))
            subtotal = discount_price * qty
            total_amount += subtotal
            prepared_items.append((g_item, qty, discount_price))

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            delivery_address=validated_data['delivery_address'],
            payment_method=validated_data.get('payment_method', 'Cash on Delivery'),
            status='Pending'
        )

        for g_item, qty, price in prepared_items:
            g_item.stock_quantity -= qty
            g_item.save()
            OrderItem.objects.create(order=order, item=g_item, quantity=qty, price=price)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role in ['Admin', 'DeliveryStaff']:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [IsAdminOrStaff]