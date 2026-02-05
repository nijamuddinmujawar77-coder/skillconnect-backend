from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    posted_ago = serializers.ReadOnlyField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location', 'category', 'job_type',
            'experience_level', 'work_mode', 'min_salary', 'max_salary',
            'salary_display', 'description', 'requirements', 'skills',
            'company_logo', 'company_size', 'created_at', 'updated_at',
            'is_active', 'posted_ago'
        ]

class JobApplicationSerializer(serializers.ModelSerializer):
    applied_ago = serializers.ReadOnlyField()
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'company_name', 'full_name', 'email', 
            'phone', 'current_position', 'experience_years', 'resume', 
            'cover_letter', 'linkedin_url', 'portfolio_url', 'expected_salary', 
            'notice_period', 'status', 'applied_at', 'applied_ago'
        ]
        read_only_fields = ['status', 'applied_at']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'job', 'full_name', 'email', 'phone', 'current_position', 
            'experience_years', 'resume', 'cover_letter', 'linkedin_url', 
            'portfolio_url', 'expected_salary', 'notice_period'
        ]