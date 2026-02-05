from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    agreed_to_terms = models.BooleanField(default=False)

    # ✅ Profile Metrics
    profile_score = models.IntegerField(default=0)
    profile_views = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    interviews_count = models.IntegerField(default=0)
    saved_jobs_count = models.IntegerField(default=0)
    bookmarked_jobs = models.IntegerField(default=0)  # ✅ Added missing field
    interview_attempts = models.IntegerField(default=0)  # ✅ Added missing field
    total_applications = models.IntegerField(default=0)  # ✅ Added missing field

    # ✅ Resume Upload
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    # ✅ Profile Picture
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # ✅ Email-based login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email


class WorkExperience(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='work_experiences')
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'
    
    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=200)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    grade = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_year']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'
    
    def __str__(self):
        return f"{self.degree} from {self.school}"


class Skill(models.Model):
    SKILL_LEVELS = [
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.IntegerField(choices=SKILL_LEVELS, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-level', 'name']
        unique_together = ['user', 'name']  # User can't have duplicate skills
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
    
    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
    
    @property
    def level_percentage(self):
        """Convert skill level (1-5) to percentage (20-100)"""
        return self.level * 20
