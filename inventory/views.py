from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist
from .models import Category, InventoryItem, StockAdjustment
from .serializers import CategorySerializer, InventoryItemSerializer, StockAdjustmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from mongoengine.errors import ValidationError


class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"User: {request.user}")  # Log the authenticated user
        if request.user.is_authenticated:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication failed"}, status=401)

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating category: {e}")
            return Response({"error": "An error occurred while creating the category."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class InventoryItemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"User: {request.user}")  # Log the authenticated user
        if request.user.is_authenticated:
            categories = InventoryItem.objects.all()
            serializer = InventoryItemSerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication failed"}, status=401)

    def post(self, request):
        print("Received data:", request.data)  # Add this line to inspect the incoming data
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"message": "Inventory item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from inventory.models import StockAdjustment, InventoryItem
from inventory.serializers import StockAdjustmentSerializer

class StockAdjustmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        adjustments = StockAdjustment.objects.all()
        serializer = StockAdjustmentSerializer(adjustments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StockAdjustmentSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.validated_data['item']
            quantity_change = int(serializer.validated_data['quantity_change'])  # Convert to int

            # Adjust stock level
            item.quantity += quantity_change
            item.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StockAdjustmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment)
        return Response(serializer.data)

    def put(self, request, pk):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        adjustment.delete()
        return Response({"message": "Stock adjustment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



from django.shortcuts import render, redirect
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using the custom user model
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Set cookies securely for both access and refresh tokens
            response = redirect('dashboard')  # Redirect after successful login
            response.set_cookie('access_token', access_token, httponly=True, secure=True)  # Secure cookies for production
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)  # Secure cookies for production

            return response
        else:
            # Invalid credentials handling
            return render(request, 'inventory/login.html', {'error': 'Invalid credentials'})

    return render(request, 'inventory/login.html')


def dashboard_view(request):
    return render(request, 'inventory/dashboard.html')


# Example views for list of categories and inventory items (may use API calls from the frontend)
class CategoryListView(TemplateView):
    template_name = 'inventory/category_list.html'


class InventoryItemListView(TemplateView):
    template_name = 'inventory/inventory_item_list.html'


class StockAdjustmentListView(TemplateView):
    template_name = 'inventory/stock_adjustment_list.html'


class CreateCategoryView(TemplateView):
    template_name = 'inventory/create_category.html'

class CreateInventoryView(TemplateView):
    template_name = 'inventory/create_inventory_item.html'

class StockAdjustmentView(TemplateView):
    template_name = 'inventory/stock_adjustment.html'


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories_count = Category.objects.count()
        inventory_items_count = InventoryItem.objects.count()
        stock_adjustments_count = StockAdjustment.objects.count()
        
        low_stock_items = InventoryItem.objects.filter(quantity__lt=10).count()  # Example threshold

        return Response({
            'categories': categories_count,
            'inventoryItems': inventory_items_count,
            'stockAdjustments': stock_adjustments_count,
            'lowStockItems': low_stock_items
        })
