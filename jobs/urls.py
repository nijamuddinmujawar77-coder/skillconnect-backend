from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job-list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('categories/', views.job_categories, name='job-categories'),
    path('stats/', views.job_stats, name='job-stats'),
    
    # Job Applications
    path('apply/', views.JobApplicationCreateView.as_view(), name='job-apply'),
    path('<int:job_id>/apply/', views.apply_to_job, name='apply-to-job'),
    path('applications/', views.JobApplicationListView.as_view(), name='my-applications'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='application-detail'),
]