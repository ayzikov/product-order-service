# installed
from django.urls import path, include
# local
from apps.orderserviceapi.views import provider_views, buyer_views


providers_patterns = [
    path("", provider_views.ProviderListCreateView.as_view(), name="list_create"),
    path("<int:provider_id>", provider_views.ProviderDetailModifyDeleteView.as_view(), name="detail")
]

buyers_patterns = [
    path("", buyer_views.BuyerRegisterView.as_view(), name="register"),
]

urlpatterns = [
    path('providers/', include((providers_patterns, 'providers'))),
    path('buyers/', include((buyers_patterns, 'buyers'))),
]

app_name = 'orderserviceapi'
