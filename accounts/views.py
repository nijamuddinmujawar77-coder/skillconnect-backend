from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.core.cache import cache
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import RegisterSerializer
from .serializers import LoginSerializer
from .serializers import ProfileSerializer, WorkExperienceSerializer, EducationSerializer, SkillSerializer
from .models import WorkExperience, Education, Skill, CustomUser

# ✅ Industry Level Performance Optimization
try:
    from core.performance import cache_result, CacheManager, PerformanceMonitor
except ImportError:
    # Fallback if performance module not available
    def cache_result(timeout=300, key_prefix=''):
        def decorator(func):
            return func
        return decorator
    
    class CacheManager:
        @classmethod
        def get_user_profile(cls, user_id): return None
        @classmethod
        def set_user_profile(cls, user_id, data, timeout=1800): pass
        @classmethod
        def invalidate_user_profile(cls, user_id): pass
    
    class PerformanceMonitor:
        @staticmethod
        def measure_query_time(func): return func



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Profile updated successfully'})
        return Response(serializer.errors, status=400)
    
    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Profile updated successfully'})
        return Response(serializer.errors, status=400)


# Work Experience Views
class WorkExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return WorkExperience.objects.filter(user=self.request.user)


# Education Views
class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Education.objects.filter(user=self.request.user)


# Skills Views
class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)


# ========== FORGOT PASSWORD VIEWS ==========
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class ForgotPasswordView(APIView):
    """Send password reset email"""
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        try:
            user = CustomUser.objects.get(email=email)
            
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            
            # Store token in cache (expires in 1 hour)
            cache_key = f'password_reset_{reset_token}'
            cache.set(cache_key, user.id, timeout=3600)  # 1 hour
            
            # Create reset link
            frontend_url = 'https://skillconnect.dev'
            reset_link = f'{frontend_url}/reset-password.html?token={reset_token}'
            
            # Send email
            try:
                send_mail(
                    subject='Reset Your SkillConnect Password',
                    message=f'''
Hi {user.first_name or 'User'},

You requested to reset your password for your SkillConnect account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email.

Best regards,
SkillConnect Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return Response({
                'message': 'If an account exists with this email, a reset link has been sent.',
                'success': True
            })
            
        except CustomUser.DoesNotExist:
            # Don't reveal if email exists or not (security)
            return Response({
                'message': 'If an account exists with this email, a reset link has been sent.',
                'success': True
            })


class ResetPasswordView(APIView):
    """Reset password with token"""
    def post(self, request):
        token = request.data.get('token', '')
        new_password = request.data.get('password', '')
        
        if not token or not new_password:
            return Response({'error': 'Token and password are required'}, status=400)
        
        if len(new_password) < 6:
            return Response({'error': 'Password must be at least 6 characters'}, status=400)
        
        # Get user from cache
        cache_key = f'password_reset_{token}'
        user_id = cache.get(cache_key)
        
        if not user_id:
            return Response({'error': 'Invalid or expired reset link'}, status=400)
        
        try:
            user = CustomUser.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            
            # Delete the token
            cache.delete(cache_key)
            
            return Response({
                'message': 'Password reset successfully! You can now login.',
                'success': True
            })
            
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)
