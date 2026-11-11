from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, GroceryItemListCreateView, GroceryItemDetailView,
    AdminOrderListView, UserOrderHistoryView, OrderCreateView,
    OrderDetailView, OrderStatusUpdateView
)

urlpatterns = [
    # Auth Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Grocery Items Endpoints
    path('items/', GroceryItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', GroceryItemDetailView.as_view(), name='item-detail'),

    # Orders Endpoints
    path('orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('orders/user/', UserOrderHistoryView.as_view(), name='user-order-history'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
]