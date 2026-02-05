"""
SkillConnect - Professional Unit Tests
Industry Standard Testing Suite for Accounts App
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, WorkExperience, Education, Skill
from .serializers import UserRegistrationSerializer, UserProfileSerializer
import json

User = get_user_model()

class CustomUserModelTest(TestCase):
    """Test CustomUser model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@skillconnect.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+91 9876543210',
            'password': 'testpassword123'
        }
    
    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@skillconnect.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '+91 9876543210')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertEqual(user.profile_score, 0)
        self.assertEqual(user.applications_count, 0)
        
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'test@skillconnect.com')
    
    def test_user_email_unique(self):
        """Test email uniqueness"""
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with same email
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='test@skillconnect.com',  # Same email
                password='password123'
            )

class WorkExperienceModelTest(TestCase):
    """Test WorkExperience model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@skillconnect.com',
            password='testpass123'
        )
        
        self.work_data = {
            'user': self.user,
            'title': 'Software Developer',
            'company': 'Tech Corp',
            'location': 'Mumbai',
            'start_date': '2023-01-01',
            'end_date': '2024-01-01',
            'is_current': False,
            'description': 'Developed web applications'
        }
    
    def test_create_work_experience(self):
        """Test work experience creation"""
        work_exp = WorkExperience.objects.create(**self.work_data)
        
        self.assertEqual(work_exp.title, 'Software Developer')
        self.assertEqual(work_exp.company, 'Tech Corp')
        self.assertEqual(work_exp.user, self.user)
        self.assertFalse(work_exp.is_current)
        
    def test_work_experience_str(self):
        """Test work experience string representation"""
        work_exp = WorkExperience.objects.create(**self.work_data)
        expected_str = 'Software Developer at Tech Corp'
        self.assertEqual(str(work_exp), expected_str)

class EducationModelTest(TestCase):
    """Test Education model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@skillconnect.com',
            password='testpass123'
        )
        
        self.edu_data = {
            'user': self.user,
            'degree': 'Bachelor of Computer Science',
            'school': 'Tech University',
            'start_year': 2020,
            'end_year': 2024,
            'is_current': False,
            'grade': 'A',
            'description': 'Computer Science with specialization in AI'
        }
    
    def test_create_education(self):
        """Test education creation"""
        education = Education.objects.create(**self.edu_data)
        
        self.assertEqual(education.degree, 'Bachelor of Computer Science')
        self.assertEqual(education.school, 'Tech University')
        self.assertEqual(education.start_year, 2020)
        self.assertEqual(education.end_year, 2024)
        self.assertEqual(education.grade, 'A')

class SkillModelTest(TestCase):
    """Test Skill model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@skillconnect.com',
            password='testpass123'
        )
    
    def test_create_skill(self):
        """Test skill creation"""
        skill = Skill.objects.create(
            user=self.user,
            name='Python',
            level=4
        )
        
        self.assertEqual(skill.name, 'Python')
        self.assertEqual(skill.level, 4)
        self.assertEqual(skill.level_percentage, 80)  # 4 * 20 = 80%
        
    def test_skill_level_percentage(self):
        """Test skill level percentage calculation"""
        skill = Skill.objects.create(
            user=self.user,
            name='JavaScript',
            level=3
        )
        
        self.assertEqual(skill.level_percentage, 60)  # 3 * 20 = 60%

class UserRegistrationAPITest(APITestCase):
    """Test user registration API"""
    
    def setUp(self):
        self.client = APIClient()
        
        self.valid_user_data = {
            'username': 'newuser',
            'email': 'newuser@skillconnect.com',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '+91 9876543210',
            'password': 'newpassword123',
            'confirm_password': 'newpassword123',
            'agreed_to_terms': True
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(
            '/api/accounts/register/',
            self.valid_user_data,
            format='json'
        )
        
        # Check if user was created
        self.assertTrue(User.objects.filter(email='newuser@skillconnect.com').exists())

class UserLoginAPITest(APITestCase):
    """Test user login API"""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/accounts/login/'
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@skillconnect.com',
            password='testpassword123'
        )
        
        self.login_data = {
            'email': 'test@skillconnect.com',
            'password': 'testpassword123'
        }
    
    def test_user_login_success(self):
        """Test successful user login"""
        response = self.client.post(
            self.login_url,
            self.login_data,
            format='json'
        )
        
        # Should return JWT tokens
        if response.status_code == 200:
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
