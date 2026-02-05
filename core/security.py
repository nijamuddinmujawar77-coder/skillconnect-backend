"""
SkillConnect - Enterprise Security Enhancements
Industry Standard Security Implementation
"""

from django.middleware.security import SecurityMiddleware
from django.http import HttpResponse
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status
import time
import hashlib
import re
from functools import wraps
from typing import Dict, Any
import logging
import base64

# Optional imports with fallbacks
try:
    from cryptography.fernet import Fernet
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    
try:
    import debug_toolbar
    DEBUG_TOOLBAR_AVAILABLE = True
except ImportError:
    DEBUG_TOOLBAR_AVAILABLE = False

# Configure security logger
security_logger = logging.getLogger('security')

class AdvancedSecurityMiddleware:
    """Advanced security middleware with industry standards"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Security headers
        response = self.get_response(request)
        
        # OWASP recommended headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # HSTS Header (only in production with HTTPS)
        if request.is_secure():
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        
        # Content Security Policy
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://api.openai.com;"
        )
        response['Content-Security-Policy'] = csp_policy
        
        return response

class RateLimitMiddleware:
    """Advanced rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_cache = {}
    
    def __call__(self, request):
        # Get client IP
        client_ip = self.get_client_ip(request)
        
        # Check rate limits
        if self.is_rate_limited(client_ip, request.path):
            return HttpResponse(
                'Rate limit exceeded. Please try again later.',
                status=429,
                content_type='application/json'
            )
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_rate_limited(self, client_ip: str, path: str) -> bool:
        """Check if client is rate limited"""
        cache_key = f"rate_limit:{client_ip}:{path}"
        
        # Get current request count
        current_requests = cache.get(cache_key, 0)
        
        # Different limits for different endpoints
        if '/api/accounts/login/' in path:
            limit = 5  # 5 login attempts per minute
            window = 60
        elif '/api/' in path:
            limit = 100  # 100 API requests per minute
            window = 60
        else:
            limit = 1000  # 1000 general requests per minute
            window = 60
        
        if current_requests >= limit:
            security_logger.warning(f"Rate limit exceeded for IP {client_ip} on {path}")
            return True
        
        # Increment counter
        cache.set(cache_key, current_requests + 1, window)
        return False

class SQLInjectionProtectionMiddleware:
    """SQL Injection detection and prevention"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.sql_injection_patterns = [
            r"(\\'|(\\')|(;)|(\\;)|(\\x27)|(\\x3D))",
            r"(\\x3D)|(\\x27)|(;)|(')|(\")|(\\x22)",
            r"(union|select|insert|delete|update|drop|create|alter|exec|execute)",
            r"(script|javascript|vbscript|onload|onerror)",
        ]
    
    def __call__(self, request):
        # Check for SQL injection attempts
        if self.detect_sql_injection(request):
            security_logger.critical(f"SQL injection attempt from {request.META.get('REMOTE_ADDR')}")
            return HttpResponse('Security violation detected', status=403)
        
        response = self.get_response(request)
        return response
    
    def detect_sql_injection(self, request) -> bool:
        """Detect potential SQL injection attempts"""
        # Check query parameters
        for key, value in request.GET.items():
            if self.contains_sql_injection(value):
                return True
        
        # Check POST data
        if hasattr(request, 'body') and request.body:
            body_str = request.body.decode('utf-8', errors='ignore')
            if self.contains_sql_injection(body_str):
                return True
        
        return False
    
    def contains_sql_injection(self, text: str) -> bool:
        """Check if text contains SQL injection patterns"""
        text_lower = text.lower()
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        return False

class APIKeySecurityMixin:
    """Mixin for API key validation"""
    
    def validate_api_key(self, request):
        """Validate API key from headers"""
        api_key = request.META.get('HTTP_X_API_KEY')
        
        if not api_key:
            return False
        
        # Check against valid API keys (store in cache/database)
        valid_keys = cache.get('valid_api_keys', [])
        return api_key in valid_keys

class SecureFileUploadMixin:
    """Secure file upload validation"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    def validate_uploaded_file(self, uploaded_file):
        """Validate uploaded file for security"""
        # Check file extension
        file_extension = uploaded_file.name.lower().split('.')[-1]
        if f'.{file_extension}' not in self.ALLOWED_EXTENSIONS:
            return False, "File type not allowed"
        
        # Check file size
        if uploaded_file.size > self.MAX_FILE_SIZE:
            return False, "File too large"
        
        # Check for malicious content (basic)
        if self.contains_malicious_content(uploaded_file):
            return False, "File contains suspicious content"
        
        return True, "File is safe"
    
    def contains_malicious_content(self, uploaded_file) -> bool:
        """Basic malicious content detection"""
        try:
            # Read first 1KB to check for suspicious patterns
            content = uploaded_file.read(1024).decode('utf-8', errors='ignore')
            uploaded_file.seek(0)  # Reset file pointer
            
            suspicious_patterns = [
                '<script', 'javascript:', 'vbscript:',
                'onload=', 'onerror=', 'eval(',
                'exec(', 'system(', 'shell_exec'
            ]
            
            content_lower = content.lower()
            for pattern in suspicious_patterns:
                if pattern in content_lower:
                    return True
        except:
            pass  # If we can't read the file, assume it's safe
        
        return False

# Custom permissions
class IsOwnerOrReadOnly(BasePermission):
    """Permission to only allow owners to edit objects"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only to the owner
        return obj.user == request.user

class IsVerifiedUser(BasePermission):
    """Permission for verified users only"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_verified', True)

# Custom throttling
class BurstRateThrottle(UserRateThrottle):
    """Burst rate limiting"""
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    """Sustained rate limiting"""
    scope = 'sustained'

# Security decorators
def require_https(view_func):
    """Decorator to require HTTPS"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.is_secure() and not settings.DEBUG:
            return HttpResponse('HTTPS required', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def log_security_event(event_type: str):
    """Decorator to log security events"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            
            security_logger.info(f"Security event: {event_type}, IP: {client_ip}, User-Agent: {user_agent}")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Encryption utilities
class DataEncryption:
    """Data encryption utilities"""
    
    @staticmethod
    def encrypt_sensitive_data(data: str) -> str:
        """Encrypt sensitive data"""
        if CRYPTOGRAPHY_AVAILABLE:
            try:
                # In production, use environment variable for key
                key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key())
                f = Fernet(key)
                
                encrypted_data = f.encrypt(data.encode())
                return base64.urlsafe_b64encode(encrypted_data).decode()
            except Exception:
                pass
        
        # Fallback - simple base64 encoding
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def decrypt_sensitive_data(encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if CRYPTOGRAPHY_AVAILABLE:
            try:
                key = getattr(settings, 'ENCRYPTION_KEY', Fernet.generate_key())
                f = Fernet(key)
                
                decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
                return f.decrypt(decoded_data).decode()
            except Exception:
                pass
        
        # Fallback - simple base64 decoding
        try:
            return base64.b64decode(encrypted_data.encode()).decode()
        except Exception:
            return encrypted_data  # Return as-is if decoding fails

# Security audit logging
class SecurityAuditLogger:
    """Comprehensive security audit logging"""
    
    @staticmethod
    def log_login_attempt(user_email: str, success: bool, ip_address: str):
        """Log login attempts"""
        status_text = "SUCCESS" if success else "FAILED"
        security_logger.info(f"Login {status_text}: {user_email} from {ip_address}")
    
    @staticmethod
    def log_permission_denied(user: Any, resource: str, ip_address: str):
        """Log permission denied events"""
        user_info = f"User:{user.email}" if user.is_authenticated else "Anonymous"
        security_logger.warning(f"Permission denied: {user_info} accessing {resource} from {ip_address}")
    
    @staticmethod
    def log_data_access(user: Any, data_type: str, action: str):
        """Log sensitive data access"""
        security_logger.info(f"Data access: {user.email} {action} {data_type}")

# Usage examples in settings.py:
"""
# Add to MIDDLEWARE
MIDDLEWARE = [
    'core.security.AdvancedSecurityMiddleware',
    'core.security.RateLimitMiddleware', 
    'core.security.SQLInjectionProtectionMiddleware',
    # ... other middleware
]

# Rate limiting settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# DRF Throttling
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'core.security.BurstRateThrottle',
        'core.security.SustainedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Encryption key (use environment variable in production)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY', 'your-encryption-key-here')
"""