"""
AI API URLs - Groq Integration
"""
from django.urls import path
from .groq_ai import GroqResumeAnalysisView, GroqDemoAnalysisView

urlpatterns = [
    path('analyze-resume/', GroqResumeAnalysisView.as_view(), name='groq-resume-analysis'),
    path('demo-analysis/', GroqDemoAnalysisView.as_view(), name='groq-demo-analysis'),
]
