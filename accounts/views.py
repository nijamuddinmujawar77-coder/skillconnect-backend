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
import threading
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import os

def send_email_with_resend(to_email, subject, html_content, text_content):
    """Send email using Resend API (works on Render free tier)"""
    try:
        resend_api_key = os.environ.get('RESEND_API_KEY')
        
        if not resend_api_key:
            print("RESEND_API_KEY not set!")
            return False
        
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {resend_api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'from': 'SkillConnect <noreply@skillconnect.dev>',
                'to': [to_email],
                'subject': subject,
                'html': html_content,
                'text': text_content
            }
        )
        
        if response.status_code == 200:
            print(f"Email sent successfully to {to_email}!")
            return True
        else:
            print(f"Email failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

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
            
            # Get user name
            user_name = user.first_name or user.email.split('@')[0]
            
            # Professional HTML Email Template
            html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f5;">
    <table role="presentation" style="width: 100%; border-collapse: collapse;">
        <tr>
            <td align="center" style="padding: 40px 0;">
                <table role="presentation" style="width: 100%; max-width: 600px; border-collapse: collapse; background-color: #ffffff; border-radius: 16px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #0d9488 0%, #f97316 100%); padding: 40px 40px; border-radius: 16px 16px 0 0; text-align: center;">
                            <table role="presentation" style="width: 100%;">
                                <tr>
                                    <td align="center">
                                        <div style="display: inline-block; background: rgba(255,255,255,0.2); padding: 12px 20px; border-radius: 12px; margin-bottom: 20px;">
                                            <span style="font-size: 28px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">💼 SkillConnect</span>
                                        </div>
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding-top: 10px;">
                                        <div style="width: 80px; height: 80px; background: rgba(255,255,255,0.95); border-radius: 50%; display: inline-block; line-height: 80px; text-align: center;">
                                            <span style="font-size: 36px;">🔐</span>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 40px;">
                            <h1 style="margin: 0 0 20px 0; font-size: 24px; font-weight: 700; color: #1f2937; text-align: center;">
                                Password Reset Request
                            </h1>
                            
                            <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.6; color: #4b5563;">
                                Hi <strong style="color: #0d9488;">{user_name}</strong>,
                            </p>
                            
                            <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.6; color: #4b5563;">
                                We received a request to reset the password for your SkillConnect account. Click the button below to create a new password:
                            </p>
                            
                            <!-- CTA Button -->
                            <table role="presentation" style="width: 100%; margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{reset_link}" style="display: inline-block; background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); color: #ffffff; text-decoration: none; padding: 16px 40px; border-radius: 12px; font-size: 16px; font-weight: 600; box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4);">
                                            🔑 Reset My Password
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Timer Warning -->
                            <table role="presentation" style="width: 100%; background: #fef3c7; border-radius: 12px; margin: 25px 0;">
                                <tr>
                                    <td style="padding: 16px 20px;">
                                        <p style="margin: 0; font-size: 14px; color: #92400e; text-align: center;">
                                            ⏰ This link will expire in <strong>1 hour</strong>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="margin: 25px 0 15px 0; font-size: 14px; color: #6b7280;">
                                If the button doesn't work, copy and paste this link into your browser:
                            </p>
                            
                            <p style="margin: 0 0 25px 0; font-size: 12px; color: #0d9488; word-break: break-all; background: #f0fdfa; padding: 12px; border-radius: 8px;">
                                {reset_link}
                            </p>
                            
                            <!-- Security Notice -->
                            <table role="presentation" style="width: 100%; background: #fef2f2; border-radius: 12px; margin-top: 25px;">
                                <tr>
                                    <td style="padding: 16px 20px;">
                                        <p style="margin: 0; font-size: 13px; color: #991b1b;">
                                            🛡️ <strong>Didn't request this?</strong> If you didn't request a password reset, please ignore this email or contact our support team. Your account is safe.
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: #f9fafb; padding: 30px 40px; border-radius: 0 0 16px 16px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="margin: 0 0 15px 0; font-size: 14px; color: #6b7280;">
                                Need help? Contact us at<br>
                                <a href="mailto:support@skillconnect.dev" style="color: #0d9488; text-decoration: none; font-weight: 600;">support@skillconnect.dev</a>
                            </p>
                            
                            <table role="presentation" style="margin: 20px auto;">
                                <tr>
                                    <td style="padding: 0 8px;"><a href="https://skillconnect.dev" style="color: #9ca3af; font-size: 20px; text-decoration: none;">🌐</a></td>
                                    <td style="padding: 0 8px;"><a href="#" style="color: #9ca3af; font-size: 20px; text-decoration: none;">📘</a></td>
                                    <td style="padding: 0 8px;"><a href="#" style="color: #9ca3af; font-size: 20px; text-decoration: none;">🐦</a></td>
                                    <td style="padding: 0 8px;"><a href="#" style="color: #9ca3af; font-size: 20px; text-decoration: none;">💼</a></td>
                                </tr>
                            </table>
                            
                            <p style="margin: 20px 0 0 0; font-size: 12px; color: #9ca3af;">
                                © 2026 SkillConnect. All rights reserved.<br>
                                India's Premier Job Platform
                            </p>
                        </td>
                    </tr>
                </table>
                
                <!-- Bottom Text -->
                <table role="presentation" style="width: 100%; max-width: 600px; margin-top: 20px;">
                    <tr>
                        <td style="text-align: center; padding: 0 20px;">
                            <p style="margin: 0; font-size: 11px; color: #9ca3af;">
                                This email was sent to {email} because a password reset was requested for this account.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
'''
            
            # Plain text fallback
            text_content = f'''
Hi {user_name},

We received a request to reset the password for your SkillConnect account.

Click the link below to reset your password:
{reset_link}

This link will expire in 1 hour.

If you didn't request this, please ignore this email. Your account is safe.

Best regards,
SkillConnect Team
support@skillconnect.dev

© 2026 SkillConnect - India's Premier Job Platform
'''
            
            # Send email using Resend API (works on Render free tier!)
            try:
                email_thread = threading.Thread(
                    target=send_email_with_resend,
                    args=(email, '🔐 Reset Your SkillConnect Password', html_content, text_content)
                )
                email_thread.start()
            except Exception as e:
                print(f"Email setup failed: {e}")
            
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
