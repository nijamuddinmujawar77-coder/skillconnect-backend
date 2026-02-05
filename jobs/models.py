from django.db import models
from django.utils import timezone
from accounts.models import CustomUser

class Job(models.Model):
    CATEGORY_CHOICES = [
        ('it', 'IT & Software'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('design', 'Design'),
        ('hr', 'HR & Admin'),
        ('sales', 'Sales'),
        ('engineering', 'Engineering'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (6-10 years)'),
        ('lead', 'Lead/Manager (10+ years)'),
    ]
    
    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('office', 'Office'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='entry')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='office')
    
    # Salary Info
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_display = models.CharField(max_length=50, help_text="e.g., ₹8-15 LPA")
    
    # Job Details
    description = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    skills = models.JSONField(default=list, help_text="List of required skills")
    
    # Company Info
    company_logo = models.CharField(max_length=10, default='🏢', help_text="Emoji for company logo")
    company_size = models.CharField(max_length=20, choices=[
        ('startup', 'Startup (1-50)'),
        ('small', 'Small (51-200)'),
        ('medium', 'Medium (201-1000)'),
        ('large', 'Large (1000+)'),
    ], default='medium')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def posted_ago(self):
        """Calculate how long ago the job was posted"""
        from django.utils.timesince import timesince
        return timesince(self.created_at)


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    
    # Relations - User field optional for now (guest applications allowed)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications', null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    
    # Application Details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    current_position = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    
    # Files
    resume = models.FileField(upload_to='applications/resumes/', help_text="Upload your resume (PDF/DOC)")
    cover_letter = models.TextField(blank=True, help_text="Tell us why you're perfect for this role")
    
    # Additional Info
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    expected_salary = models.CharField(max_length=50, blank=True)
    notice_period = models.CharField(max_length=100, blank=True, help_text="e.g., Immediate, 1 month, 2 months")
    
    # Status & Tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # HR Notes (Internal use)
    hr_notes = models.TextField(blank=True, help_text="Internal notes for HR team")
    
    class Meta:
        ordering = ['-applied_at']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
    
    def __str__(self):
        return f"{self.full_name} applied for {self.job.title} at {self.job.company}"
    
    @property
    def applied_ago(self):
        """Calculate how long ago the application was submitted"""
        from django.utils.timesince import timesince
        return timesince(self.applied_at)
    CATEGORY_CHOICES = [
        ('it', 'IT & Software'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('design', 'Design'),
        ('hr', 'HR & Admin'),
        ('sales', 'Sales'),
        ('engineering', 'Engineering'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (3-5 years)'),
        ('senior', 'Senior Level (6-10 years)'),
        ('lead', 'Lead/Manager (10+ years)'),
    ]
    
    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('office', 'Office'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full-time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='entry')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='office')
    
    # Salary Info
    min_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_display = models.CharField(max_length=50, help_text="e.g., ₹8-15 LPA")
    
    # Job Details
    description = models.TextField()
    requirements = models.TextField(null=True, blank=True)
    skills = models.JSONField(default=list, help_text="List of required skills")
    
    # Company Info
    company_logo = models.CharField(max_length=10, default='🏢', help_text="Emoji for company logo")
    company_size = models.CharField(max_length=20, choices=[
        ('startup', 'Startup (1-50)'),
        ('small', 'Small (51-200)'),
        ('medium', 'Medium (201-1000)'),
        ('large', 'Large (1000+)'),
    ], default='medium')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def posted_ago(self):
        """Calculate how long ago the job was posted"""
        from django.utils.timesince import timesince
        return timesince(self.created_at)
