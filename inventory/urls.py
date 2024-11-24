from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Categories
    path('categories/', views.CategoryView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Inventory Items
    path('inventory-items/', views.InventoryItemView.as_view(), name='inventory-item-list'),
    path('inventory-items/<int:pk>/', views.InventoryItemDetailView.as_view(), name='inventory-item-detail'),

    # Stock Adjustments
    path('stock-adjustments/', views.StockAdjustmentAPIView.as_view(), name='stock-adjustment-list'),
    path('stock-adjustments/<int:pk>/', views.StockAdjustmentDetailView.as_view(), name='stock-adjustment-detail'),

    # path('login/', views.CustomLoginView.as_view(), name='login-user'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Categories, Inventory Items, Stock Adjustments
    # path('categories-tm/', views.CategoryListView.as_view(), name='category-list-tm'),
    # path('inventory-tm/', views.InventoryItemListView.as_view(), name='inventory-item-list-tm'),
    # path('stock-adjustments-tm/', views.StockAdjustmentListView.as_view(), name='stock-adjustment-list-tm'),
    path('api/dashboard-stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('admin/categories/', views.CategoryListView.as_view(), name='manage-categories'),
    path('admin/inventory-items/', views.InventoryItemListView.as_view(), name='manage-inventory-items'),
    path('admin/stock-adjustments/', views.StockAdjustmentListView.as_view(), name='manage-stock-adjustments'),
    path('categories/create/', views.CreateCategoryView.as_view(), name='create-category'),
    path('inventory/create/', views.CreateInventoryView.as_view(), name='create-inventory'),
    path('stock-adjustments/adjust/', views.StockAdjustmentView.as_view(), name='stock-adjustments'),
]
