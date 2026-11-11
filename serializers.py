from rest_framework import serializers
from .models import User, GroceryItem, Order, OrderItem

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Customer')
        )
        return user


class GroceryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroceryItem
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'item_name', 'quantity', 'price']


class OrderItemInputSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    delivery_address = serializers.CharField()
    payment_method = serializers.CharField(default='Cash on Delivery')
    items = OrderItemInputSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='user.username', read_only=True)
    customer_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'customer_name', 'customer_email', 'status', 'total_amount', 'delivery_address', 'payment_method', 'payment_status', 'created_at', 'items']
        read_only_fields = ['user', 'total_amount', 'status']


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status', 'payment_status']