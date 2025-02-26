# installed
from django.urls import path, include
from unicodedata import category

# local
from apps.orderserviceapi.views import provider_views, buyer_views, product_views, order_views, category_views


buyers_patterns = [
    path("", buyer_views.BuyerRegisterView.as_view(), name="register"),
    path('confirm-email/<str:token>/<str:uid>', buyer_views.BuyerConfirmEmailView.as_view(), name="confirm_email"),
]

categories_patterns = [
    path("", category_views.CategoryCreateView.as_view(), name="create"),
]

orders_patterns = [
    path("", order_views.OrderListCreateView.as_view(), name="list_create"),
    path("<int:order_id>", order_views.OrderDetailModifyDeleteView.as_view(), name="detail_modify_delete"),
    path("<int:order_id>/confirm", order_views.OrderConfirmView.as_view(), name="confirm"),
    path("<int:order_id>/cancel", order_views.OrderCancelView.as_view(), name="cancel"),
    path("<int:order_id>/product/<int:product_id>", order_views.OrderAddProductView.as_view(), name="add_product"),
]

products_patterns = [
    path("", product_views.ProductListCreateView.as_view(), name="list_create"),
    path("<int:product_id>", product_views.ProductDetailModifyDeleteView.as_view(), name="detail_modify_delete"),
    path("<int:product_id>/stock", product_views.ProductStockView.as_view(), name="stock")
]

providers_patterns = [
    path("", provider_views.ProviderListCreateView.as_view(), name="list_create"),
    path("<int:provider_id>", provider_views.ProviderDetailModifyDeleteView.as_view(), name="detail_modify_delete")
]


urlpatterns = [
    path('buyers/', include((buyers_patterns, 'buyers'))),
    path('categories/', include((categories_patterns, 'categories'))),
    path('orders/', include((orders_patterns, 'orders'))),
    path('products/', include((products_patterns, 'products'))),
    path('providers/', include((providers_patterns, 'providers'))),
]

app_name = 'orderserviceapi'
