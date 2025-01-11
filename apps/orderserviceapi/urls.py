# installed
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# local
from apps.orderserviceapi.views.provider_views import ProviderListView, ProviderDetailView
from apps.orderserviceapi.views.product_views import ProductListView, ProductDetailView
from apps.orderserviceapi.views.category_views import CategoryListView, CategoryDetailView


# router = DefaultRouter()
# router.register(r'providers', ProviderViewSet, basename='providers')

urlpatterns = [
    # path('', include(router.urls)),

    path('categories/', CategoryListView.as_view()),
    path('categories/<int:id>', CategoryDetailView.as_view()),
    # path('orders/', ),
    path('products/', ProductListView.as_view()),
    path('products/<int:id>', ProductDetailView.as_view()),
    # path('products/', ), # добавить товар на склад (нужно переделать эндпоинт)
    path('providers/', ProviderListView.as_view()),
    path('providers/<int:id>', ProviderDetailView.as_view()),
    # path('users/register/', ),
]

app_name = 'orderserviceapi'
