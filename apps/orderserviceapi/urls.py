# installed
from django.urls import path, include
# local
from apps.orderserviceapi.views import provider_views


providers_patterns = [
    path("", provider_views.ProviderListCreateView.as_view(), name="list_create"),
    path("<int:provider_id>", provider_views.ProviderDetailModifyDeleteView.as_view(), name="detail")
]

urlpatterns = [
    path('providers/', include((providers_patterns, 'providers'))),
]

app_name = 'orderserviceapi'
