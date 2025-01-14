# installed
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# local
from apps.orderserviceapi.views.provider_views import ProviderListView, ProviderDetailView
from apps.orderserviceapi.views.product_views import ProductListView, ProductDetailView, ProductWarehouseView
from apps.orderserviceapi.views.category_views import CategoryListView, CategoryDetailView
from apps.orderserviceapi.views.buyer_views import BuyerView, BuyerConfirmEmailView
from apps.orderserviceapi.views.order_views import OrderView


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:id>', CategoryDetailView.as_view()),

    path('orders/', OrderView.as_view()),

    path('products/', ProductListView.as_view()),
    path('products/<int:id>', ProductDetailView.as_view()),
    path('products/<int:id>/warehouse/', ProductWarehouseView.as_view()),

    path('providers/', ProviderListView.as_view()),
    path('providers/<int:id>', ProviderDetailView.as_view()),

    path('users/', BuyerView.as_view()),
    path('confirm-email/<str:token>/<str:uidb64>', BuyerConfirmEmailView.as_view()),
]

app_name = 'orderserviceapi'
