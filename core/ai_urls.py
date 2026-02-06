"""
AI API URLs - Groq Integration
"""
from django.urls import path
from .groq_ai import (
    GroqResumeAnalysisView, 
    GroqDemoAnalysisView,
    GroqJobMatchView,
    GroqInterviewFeedbackView
)

urlpatterns = [
    # Resume Analysis
    path('analyze-resume/', GroqResumeAnalysisView.as_view(), name='groq-resume-analysis'),
    path('demo-analysis/', GroqDemoAnalysisView.as_view(), name='groq-demo-analysis'),
    
    # Job Match Analysis
    path('job-match/', GroqJobMatchView.as_view(), name='groq-job-match'),
    
    # Interview Feedback
    path('interview-feedback/', GroqInterviewFeedbackView.as_view(), name='groq-interview-feedback'),
]
