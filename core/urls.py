"""
URL configuration for core project - Industry Level API Documentation
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Optional imports with fallbacks
try:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    SWAGGER_AVAILABLE = True
except ImportError:
    SWAGGER_AVAILABLE = False

# Only create schema if packages are available
if SWAGGER_AVAILABLE:
    # ✅ Professional API Documentation Schema
    schema_view = get_schema_view(
        openapi.Info(
            title="SkillConnect API",
            default_version='v1',
            description="""
            🚀 **Professional Career Platform API**
            
            Complete REST API for SkillConnect - India's comprehensive career development platform.
            
            ## Features:
            - 🔐 JWT Authentication System
            - 👤 User Profile Management  
            - 💼 Job Search & Applications
            - 🛠️ 13 Career Development Tools
            - 📱 Mobile-First Design
            
            ## Authentication:
            Use JWT Bearer tokens: `Authorization: Bearer <your-token>`
            
            ## Rate Limits:
            - Authenticated users: 1000 requests/hour
            - Anonymous users: 100 requests/hour
            """,
            terms_of_service="https://skillconnect.com/terms/",
            contact=openapi.Contact(
                email="api@skillconnect.com",
                url="https://skillconnect.com/contact/"
            ),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

# 🔧 Temporary setup view for creating superuser
from django.http import JsonResponse
from accounts.models import CustomUser

def setup_admin(request):
    """Temporary endpoint to create superuser - DELETE AFTER USE"""
    email = 'nijamuddinmujawar77@gmail.com'
    password = 'admin123'
    
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'status': 'exists', 'message': f'Superuser already exists: {email}'})
    
    user = CustomUser.objects.create_superuser(
        email=email,
        password=password,
        first_name='Nijamuddin',
        last_name='Mujawar'
    )
    return JsonResponse({'status': 'created', 'message': f'Superuser created: {email}'})

urlpatterns = [
    # 🔧 Admin interface
    path('admin/', admin.site.urls),
    
    # 🚨 TEMPORARY - Setup endpoint (DELETE AFTER USE)
    path('setup-admin/', setup_admin, name='setup-admin'),
    
    # 📋 API routes
    path('api/accounts/', include('accounts.urls')),
    path('api/newsletter/', include('newsletter.urls')),
    path('api/jobs/', include('jobs.urls')),
]

# Add API documentation URLs only if available
if SWAGGER_AVAILABLE:
    urlpatterns += [
        # 📚 Professional API Documentation
        path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs-swagger'),
        path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-docs-redoc'),
        path('api/schema.json', schema_view.without_ui(cache_timeout=0), name='api-schema-json'),
    ]

# ✅ Development configurations
if settings.DEBUG:
    # Media files serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar (Industry standard development tool)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass  # Debug toolbar not installed - no problem
