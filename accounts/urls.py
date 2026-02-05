from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    WorkExperienceListCreateView, WorkExperienceDetailView,
    EducationListCreateView, EducationDetailView,
    SkillListCreateView, SkillDetailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Work Experience URLs
    path('experience/', WorkExperienceListCreateView.as_view(), name='experience-list-create'),
    path('experience/<int:pk>/', WorkExperienceDetailView.as_view(), name='experience-detail'),
    
    # Education URLs
    path('education/', EducationListCreateView.as_view(), name='education-list-create'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
    
    # Skills URLs
    path('skills/', SkillListCreateView.as_view(), name='skills-list-create'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skills-detail'),
]
