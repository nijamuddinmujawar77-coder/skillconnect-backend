"""
SkillConnect - Performance Optimization Module
Industry Standard Database Query Optimization & Caching
"""

from django.core.cache import cache
from django.db import models
from django.conf import settings
from functools import wraps
import time
import hashlib
import json

class PerformanceOptimizedManager(models.Manager):
    """Custom manager with query optimization"""
    
    def get_optimized_queryset(self):
        """Get optimized queryset with select_related and prefetch_related"""
        return self.select_related().prefetch_related()
    
    def bulk_create_optimized(self, objs, batch_size=1000):
        """Optimized bulk creation with batching"""
        return self.bulk_create(objs, batch_size=batch_size, ignore_conflicts=True)

def cache_result(timeout=300, key_prefix='skillconnect'):
    """
    Decorator for caching function results
    Usage: @cache_result(timeout=600, key_prefix='user_profile')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{key_prefix}:{func.__name__}:{hashlib.md5(str(args).encode() + str(kwargs).encode()).hexdigest()}"
            
            # Try to get from cache first
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # If not in cache, execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout=timeout)
            return result
        return wrapper
    return decorator

class QueryOptimizer:
    """Database query optimization utilities"""
    
    @staticmethod
    def optimize_user_profile_query(user_id):
        """Optimized query for user profile with related data"""
        from accounts.models import CustomUser
        
        return CustomUser.objects.select_related().prefetch_related(
            'work_experiences',
            'educations', 
            'skills'
        ).get(id=user_id)
    
    @staticmethod
    def optimize_job_listing_query(filters=None):
        """Optimized query for job listings with filters"""
        from jobs.models import Job
        
        queryset = Job.objects.select_related('company').filter(is_active=True)
        
        if filters:
            if 'location' in filters:
                queryset = queryset.filter(location__icontains=filters['location'])
            if 'job_type' in filters:
                queryset = queryset.filter(job_type=filters['job_type'])
            if 'min_salary' in filters:
                queryset = queryset.filter(salary_min__gte=filters['min_salary'])
        
        return queryset.order_by('-posted_date')[:50]  # Limit results

class CacheManager:
    """Centralized cache management"""
    
    USER_PROFILE_CACHE_KEY = 'user_profile_{}'
    JOB_LISTINGS_CACHE_KEY = 'job_listings_{}'
    POPULAR_JOBS_CACHE_KEY = 'popular_jobs'
    
    @classmethod
    def get_user_profile(cls, user_id):
        """Get cached user profile"""
        cache_key = cls.USER_PROFILE_CACHE_KEY.format(user_id)
        return cache.get(cache_key)
    
    @classmethod
    def set_user_profile(cls, user_id, profile_data, timeout=1800):  # 30 minutes
        """Cache user profile data"""
        cache_key = cls.USER_PROFILE_CACHE_KEY.format(user_id)
        cache.set(cache_key, profile_data, timeout=timeout)
    
    @classmethod
    def invalidate_user_profile(cls, user_id):
        """Invalidate user profile cache when updated"""
        cache_key = cls.USER_PROFILE_CACHE_KEY.format(user_id)
        cache.delete(cache_key)
    
    @classmethod
    def get_job_listings(cls, filters_hash):
        """Get cached job listings"""
        cache_key = cls.JOB_LISTINGS_CACHE_KEY.format(filters_hash)
        return cache.get(cache_key)
    
    @classmethod
    def set_job_listings(cls, filters_hash, job_data, timeout=600):  # 10 minutes
        """Cache job listings"""
        cache_key = cls.JOB_LISTINGS_CACHE_KEY.format(filters_hash)
        cache.set(cache_key, job_data, timeout=timeout)

class DatabaseIndexOptimizer:
    """Database index optimization suggestions"""
    
    RECOMMENDED_INDEXES = {
        'accounts_customuser': [
            'CREATE INDEX idx_user_email ON accounts_customuser(email);',
            'CREATE INDEX idx_user_active ON accounts_customuser(is_active, date_joined);',
            'CREATE INDEX idx_user_location ON accounts_customuser(location);',
        ],
        'jobs_job': [
            'CREATE INDEX idx_job_active ON jobs_job(is_active, posted_date);',
            'CREATE INDEX idx_job_location ON jobs_job(location);',
            'CREATE INDEX idx_job_type ON jobs_job(job_type, work_mode);',
            'CREATE INDEX idx_job_salary ON jobs_job(salary_min, salary_max);',
            'CREATE INDEX idx_job_search ON jobs_job(location, job_type, is_active);',
        ],
        'jobs_jobapplication': [
            'CREATE INDEX idx_application_user ON jobs_jobapplication(user_id, applied_date);',
            'CREATE INDEX idx_application_job ON jobs_jobapplication(job_id, status);',
        ],
        'accounts_workexperience': [
            'CREATE INDEX idx_work_user ON accounts_workexperience(user_id, start_date);',
        ],
        'accounts_education': [
            'CREATE INDEX idx_education_user ON accounts_education(user_id, start_year);',
        ]
    }
    
    @classmethod
    def generate_index_sql(cls):
        """Generate SQL for creating recommended indexes"""
        sql_statements = []
        for table, indexes in cls.RECOMMENDED_INDEXES.items():
            sql_statements.extend(indexes)
        return sql_statements

class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    @staticmethod
    def measure_query_time(func):
        """Decorator to measure query execution time"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            if execution_time > 1.0:  # Log slow queries (>1 second)
                import logging
                logger = logging.getLogger('performance')
                logger.warning(f"Slow query detected: {func.__name__} took {execution_time:.2f}s")
            
            return result
        return wrapper
    
    @staticmethod
    def log_cache_hit_rate():
        """Log cache hit rates for monitoring"""
        # This would integrate with Redis or cache backend
        pass

class LazyLoadingMixin:
    """Mixin for implementing lazy loading in views"""
    
    def get_paginated_response_lazy(self, data, page_size=20):
        """Implement lazy loading pagination"""
        from django.core.paginator import Paginator
        
        paginator = Paginator(data, page_size)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        return {
            'results': page_obj.object_list,
            'count': paginator.count,
            'next': page_obj.has_next(),
            'previous': page_obj.has_previous(),
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number
        }

# Performance optimization utilities
def optimize_image_upload(image_file, max_size=(800, 600), quality=85):
    """Optimize uploaded images for performance"""
    from PIL import Image
    import io
    
    if image_file.size > 1024 * 1024:  # If larger than 1MB
        img = Image.open(image_file)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        return output
    
    return image_file

def batch_database_operations(operations, batch_size=100):
    """Batch database operations for better performance"""
    from django.db import transaction
    
    with transaction.atomic():
        for i in range(0, len(operations), batch_size):
            batch = operations[i:i + batch_size]
            for operation in batch:
                operation()

# Example usage in views:
"""
# In your views.py:

from .performance import cache_result, CacheManager, QueryOptimizer

class OptimizedUserProfileView(APIView):
    
    @cache_result(timeout=1800, key_prefix='user_profile')
    def get_user_profile_data(self, user_id):
        return QueryOptimizer.optimize_user_profile_query(user_id)
    
    def get(self, request):
        user_id = request.user.id
        
        # Try cache first
        profile_data = CacheManager.get_user_profile(user_id)
        if not profile_data:
            profile_data = self.get_user_profile_data(user_id)
            CacheManager.set_user_profile(user_id, profile_data)
        
        serializer = UserProfileSerializer(profile_data)
        return Response(serializer.data)
"""