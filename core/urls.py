"""
URL configuration for core project - Industry Level API Documentation
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# ✅ Custom Admin Panel Branding
admin.site.site_header = 'SkillConnect Admin Panel'
admin.site.site_title = 'SkillConnect Admin'
admin.site.index_title = 'Welcome to SkillConnect Administration'

# Optional imports with fallbacks
try:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi
    SWAGGER_AVAILABLE = True
except ImportError:
    SWAGGER_AVAILABLE = False

# Only create schema if packages are available
if SWAGGER_AVAILABLE:
    # ✅ Professional API Documentation Schema
    schema_view = get_schema_view(
        openapi.Info(
            title="SkillConnect API",
            default_version='v1',
            description="""
            🚀 **Professional Career Platform API**
            
            Complete REST API for SkillConnect - India's comprehensive career development platform.
            
            ## Features:
            - 🔐 JWT Authentication System
            - 👤 User Profile Management  
            - 💼 Job Search & Applications
            - 🛠️ 13 Career Development Tools
            - 📱 Mobile-First Design
            
            ## Authentication:
            Use JWT Bearer tokens: `Authorization: Bearer <your-token>`
            
            ## Rate Limits:
            - Authenticated users: 1000 requests/hour
            - Anonymous users: 100 requests/hour
            """,
            terms_of_service="https://skillconnect.com/terms/",
            contact=openapi.Contact(
                email="api@skillconnect.com",
                url="https://skillconnect.com/contact/"
            ),
            license=openapi.License(name="MIT License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

# 🔧 Temporary setup view for creating superuser
from django.http import JsonResponse
from accounts.models import CustomUser
from jobs.models import Job

def setup_admin(request):
    """Temporary endpoint to create superuser - DELETE AFTER USE"""
    email = 'nijamuddinmujawar77@gmail.com'
    password = 'admin123'
    username = 'admin'
    
    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({'status': 'exists', 'message': f'Superuser already exists: {email}'})
    
    user = CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password=password,
        first_name='Nijamuddin',
        last_name='Mujawar'
    )
    return JsonResponse({'status': 'created', 'message': f'Superuser created: {email}'})

def setup_jobs(request):
    """Temporary endpoint to add sample jobs - DELETE AFTER USE"""
    jobs_data = [
        {"title": "Frontend Developer", "company": "TCS", "location": "Mumbai, India", "category": "it", "job_type": "full-time", "experience_level": "entry", "work_mode": "hybrid", "min_salary": 400000, "max_salary": 700000, "salary_display": "₹4-7 LPA", "description": "Build user-friendly web applications using React.js and modern JavaScript.", "requirements": "Bachelor's in CS. Strong HTML, CSS, JavaScript. React.js experience.", "skills": ["React.js", "JavaScript", "HTML", "CSS"], "company_logo": "🏢", "company_size": "large"},
        {"title": "Python Developer", "company": "Infosys", "location": "Bangalore, India", "category": "it", "job_type": "full-time", "experience_level": "mid", "work_mode": "office", "min_salary": 800000, "max_salary": 1200000, "salary_display": "₹8-12 LPA", "description": "Build scalable backend systems with Django and cloud technologies.", "requirements": "3+ years Python. Django/Flask knowledge. REST APIs experience.", "skills": ["Python", "Django", "REST API", "PostgreSQL"], "company_logo": "💻", "company_size": "large"},
        {"title": "Data Analyst", "company": "Wipro", "location": "Pune, India", "category": "it", "job_type": "full-time", "experience_level": "entry", "work_mode": "hybrid", "min_salary": 500000, "max_salary": 800000, "salary_display": "₹5-8 LPA", "description": "Analyze datasets and create dashboards using Power BI and Python.", "requirements": "SQL, Python, Excel. Data visualization experience.", "skills": ["Python", "SQL", "Power BI", "Excel"], "company_logo": "📊", "company_size": "large"},
        {"title": "Digital Marketing Executive", "company": "Zomato", "location": "Gurugram, India", "category": "marketing", "job_type": "full-time", "experience_level": "entry", "work_mode": "office", "min_salary": 300000, "max_salary": 500000, "salary_display": "₹3-5 LPA", "description": "Drive digital marketing campaigns across social media and Google Ads.", "requirements": "SEO, SEM, Social Media Marketing knowledge.", "skills": ["SEO", "Google Ads", "Social Media", "Analytics"], "company_logo": "🍕", "company_size": "medium"},
        {"title": "Backend Developer Intern", "company": "SkillConnect Labs", "location": "Remote", "category": "it", "job_type": "internship", "experience_level": "entry", "work_mode": "remote", "min_salary": 10000, "max_salary": 20000, "salary_display": "₹10-20K/month", "description": "Learn and work on real projects. Build APIs using Django.", "requirements": "CS/IT student. Basic Python or JavaScript knowledge.", "skills": ["Python", "Django", "Git", "REST API"], "company_logo": "🚀", "company_size": "startup"},
        {"title": "UI/UX Designer", "company": "Flipkart", "location": "Bangalore, India", "category": "design", "job_type": "full-time", "experience_level": "mid", "work_mode": "hybrid", "min_salary": 1000000, "max_salary": 1500000, "salary_display": "₹10-15 LPA", "description": "Design beautiful user interfaces for e-commerce platform.", "requirements": "3+ years UI/UX. Figma proficiency. Strong portfolio.", "skills": ["Figma", "Adobe XD", "User Research", "Prototyping"], "company_logo": "🛒", "company_size": "large"},
        {"title": "HR Executive", "company": "Reliance Industries", "location": "Mumbai, India", "category": "hr", "job_type": "full-time", "experience_level": "entry", "work_mode": "office", "min_salary": 350000, "max_salary": 500000, "salary_display": "₹3.5-5 LPA", "description": "Handle recruitment, onboarding, and HR operations.", "requirements": "MBA in HR. Good communication skills.", "skills": ["Recruitment", "Employee Relations", "Payroll", "MS Office"], "company_logo": "🏭", "company_size": "large"},
        {"title": "Full Stack Developer", "company": "Amazon", "location": "Hyderabad, India", "category": "it", "job_type": "full-time", "experience_level": "senior", "work_mode": "hybrid", "min_salary": 2500000, "max_salary": 4000000, "salary_display": "₹25-40 LPA", "description": "Build large-scale distributed systems with React and Node.js.", "requirements": "6+ years full stack experience. Microservices knowledge.", "skills": ["React", "Node.js", "AWS", "MongoDB"], "company_logo": "📦", "company_size": "large"},
        {"title": "Content Writer", "company": "Times of India", "location": "Delhi, India", "category": "marketing", "job_type": "full-time", "experience_level": "entry", "work_mode": "office", "min_salary": 200000, "max_salary": 400000, "salary_display": "₹2-4 LPA", "description": "Write engaging articles, blogs, and SEO-optimized content.", "requirements": "Excellent writing skills. SEO knowledge.", "skills": ["Content Writing", "SEO", "Research", "Editing"], "company_logo": "📰", "company_size": "large"},
        {"title": "Sales Executive", "company": "HDFC Bank", "location": "Solapur, India", "category": "sales", "job_type": "full-time", "experience_level": "entry", "work_mode": "office", "min_salary": 250000, "max_salary": 400000, "salary_display": "₹2.5-4 LPA", "description": "Sell banking products and meet monthly sales targets.", "requirements": "Graduate. Good communication. Field work.", "skills": ["Sales", "Communication", "Negotiation", "Banking"], "company_logo": "🏦", "company_size": "large"},
    ]
    
    count = 0
    for job_data in jobs_data:
        job, created = Job.objects.get_or_create(
            title=job_data["title"],
            company=job_data["company"],
            defaults=job_data
        )
        if created:
            count += 1
    
    return JsonResponse({'status': 'success', 'message': f'{count} new jobs added. Total: {Job.objects.count()}'})

urlpatterns = [
    # 🏠 Root redirect to admin panel (for admin.skillconnect.dev)
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    
    # 🔧 Admin interface
    path('admin/', admin.site.urls),
    
    # 🚨 TEMPORARY - Setup endpoints (DELETE AFTER USE)
    path('setup-admin/', setup_admin, name='setup-admin'),
    path('setup-jobs/', setup_jobs, name='setup-jobs'),
    
    # 📋 API routes
    path('api/accounts/', include('accounts.urls')),
    path('api/newsletter/', include('newsletter.urls')),
    path('api/jobs/', include('jobs.urls')),
    
    # 🤖 AI Resume Analysis (Groq - FREE)
    path('api/ai/', include('core.ai_urls')),
]

# Add API documentation URLs only if available
if SWAGGER_AVAILABLE:
    urlpatterns += [
        # 📚 Professional API Documentation
        path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs-swagger'),
        path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api-docs-redoc'),
        path('api/schema.json', schema_view.without_ui(cache_timeout=0), name='api-schema-json'),
    ]

# ✅ Development configurations
if settings.DEBUG:
    # Media files serving
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Debug toolbar (Industry standard development tool)
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass  # Debug toolbar not installed - no problem
