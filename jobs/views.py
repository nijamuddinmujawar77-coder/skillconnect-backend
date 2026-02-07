from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer, JobApplicationCreateSerializer

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created_at', 'title', 'company', 'min_salary']
    ordering = ['-created_at']
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        
        # Category filtering
        category = self.request.query_params.get('category')
        if category and category != '':
            queryset = queryset.filter(category=category)
        
        # Job type filtering
        job_type = self.request.query_params.get('job_type')
        if job_type:
            queryset = queryset.filter(job_type=job_type)
            
        # Experience level filtering
        experience_level = self.request.query_params.get('experience_level')
        if experience_level:
            queryset = queryset.filter(experience_level=experience_level)
            
        # Work mode filtering
        work_mode = self.request.query_params.get('work_mode')
        if work_mode:
            queryset = queryset.filter(work_mode=work_mode)
        
        # Custom filtering for salary range
        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')
        
        if min_salary:
            queryset = queryset.filter(min_salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(max_salary__lte=max_salary)
            
        # Custom search for keywords
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) |
                Q(company__icontains=keyword) |
                Q(description__icontains=keyword)
            )
            
        # Location filtering
        location = self.request.query_params.get('location')
        if location and location.lower() != 'all':
            queryset = queryset.filter(location__icontains=location)
            
        return queryset

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer

@api_view(['GET'])
def job_categories(request):
    """Get all available job categories"""
    categories = [{'value': choice[0], 'label': choice[1]} for choice in Job.CATEGORY_CHOICES]
    return Response(categories)

@api_view(['GET'])
def job_stats(request):
    """Get job statistics"""
    total_jobs = Job.objects.filter(is_active=True).count()
    categories_count = Job.objects.filter(is_active=True).values('category').distinct().count()
    companies_count = Job.objects.filter(is_active=True).values('company').distinct().count()
    
    return Response({
        'total_jobs': total_jobs,
        'categories': categories_count,
        'companies': companies_count
    })

# Job Application Views
class JobApplicationCreateView(generics.CreateAPIView):
    serializer_class = JobApplicationCreateSerializer
    # No authentication required - guest applications allowed
    
    def perform_create(self, serializer):
        # Only set user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

class JobApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

@api_view(['POST'])
def apply_to_job(request, job_id):
    """Apply to a specific job"""
    try:
        job = Job.objects.get(id=job_id, is_active=True)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check for duplicate application by email
    email = request.data.get('email')
    if email:
        existing_application = JobApplication.objects.filter(
            job=job, email=email
        ).first()
        
        if existing_application:
            return Response({
                'error': 'An application with this email already exists for this job'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create application
    data = request.data.copy()
    data['job'] = job_id
    
    serializer = JobApplicationCreateSerializer(data=data)
    if serializer.is_valid():
        # Link application to user if authenticated
        if request.user.is_authenticated:
            application = serializer.save(user=request.user)
        else:
            application = serializer.save()
        return Response({
            'success': True,
            'message': 'Application submitted successfully!',
            'application_id': application.id,
            'job_title': job.title,
            'company': job.company
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
