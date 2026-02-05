from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'category', 'location', 'job_type', 'salary_display', 'created_at', 'is_active']
    list_display_links = ['title', 'company']  # Make title and company clickable for editing
    list_filter = ['category', 'job_type', 'experience_level', 'work_mode', 'company_size', 'is_active']
    search_fields = ['title', 'company', 'location', 'description']
    ordering = ['-created_at']
    list_editable = ['is_active']
    actions_on_top = True
    actions_on_bottom = True
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company', 'location', 'category', 'job_type', 'experience_level', 'work_mode')
        }),
        ('Salary Information', {
            'fields': ('min_salary', 'max_salary', 'salary_display')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'skills')
        }),
        ('Company Information', {
            'fields': ('company_logo', 'company_size')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job', 'status', 'experience_years', 'applied_at']
    list_filter = ['status', 'job__category', 'experience_years', 'applied_at']
    search_fields = ['full_name', 'email', 'job__title', 'job__company']
    ordering = ['-applied_at']
    list_editable = ['status']
    readonly_fields = ['applied_at', 'updated_at']
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'job', 'status', 'applied_at', 'updated_at')
        }),
        ('Personal Details', {
            'fields': ('full_name', 'email', 'phone', 'current_position', 'experience_years')
        }),
        ('Application Materials', {
            'fields': ('resume', 'cover_letter')
        }),
        ('Additional Information', {
            'fields': ('linkedin_url', 'portfolio_url', 'expected_salary', 'notice_period')
        }),
        ('HR Notes', {
            'fields': ('hr_notes',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'job')
