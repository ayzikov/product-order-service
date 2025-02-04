# installed
from django.urls import path, include
# local
from apps.orderserviceapi.views import provider_views, buyer_views, product_views


products_patterns = [
    path("", product_views.ProductListCreateView.as_view(), name="list_create"),
    path("<int:product_id>", product_views.ProductDetailModifyDeleteView.as_view(), name="detail_modify_delete"),
    path("<int:product_id>/stock", product_views.ProductStockView.as_view(), name="stock")
]

providers_patterns = [
    path("", provider_views.ProviderListCreateView.as_view(), name="list_create"),
    path("<int:provider_id>", provider_views.ProviderDetailModifyDeleteView.as_view(), name="detail_modify_delete")
]

buyers_patterns = [
    path("", buyer_views.BuyerRegisterView.as_view(), name="register"),
    path('confirm-email/<str:token>/<str:uid>', buyer_views.BuyerConfirmEmailView.as_view(), name="confirm_email"),
]

urlpatterns = [
    path('products/', include((products_patterns, 'products'))),
    path('providers/', include((providers_patterns, 'providers'))),
    path('buyers/', include((buyers_patterns, 'buyers'))),
]

app_name = 'orderserviceapi'
