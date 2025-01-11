from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('apps.orderserviceapi.urls', namespace='orderserviceapi')),
    path('admin/', admin.site.urls),
]
