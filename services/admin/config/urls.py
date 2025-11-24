"""
URL Configuration for Swap Admin Service.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

# Admin site customization
admin.site.site_header = 'Swap Platform Administration'
admin.site.site_title = 'Swap Admin'
admin.site.index_title = 'Welcome to Swap Administration'

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('health/', lambda request: JsonResponse({'status': 'healthy'})),
]
