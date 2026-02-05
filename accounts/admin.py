from django.contrib import admin
from .models import CustomUser, WorkExperience, Education, Skill

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'company', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date', 'company']
    search_fields = ['title', 'company', 'user__email']
    ordering = ['-start_date']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['user', 'degree', 'school', 'start_year', 'end_year', 'is_current']
    list_filter = ['is_current', 'start_year', 'school']
    search_fields = ['degree', 'school', 'user__email']
    ordering = ['-start_year']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'level', 'get_level_display', 'level_percentage']
    list_filter = ['level', 'created_at']
    search_fields = ['name', 'user__email']
    ordering = ['user', '-level', 'name']
    
    def level_percentage(self, obj):
        return f"{obj.level_percentage}%"
    level_percentage.short_description = 'Level %'
