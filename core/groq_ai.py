"""
SkillConnect - Groq AI Integration (FREE & FAST)
Resume Analysis using Groq's Llama 3.3 70B Model
"""

import json
import re
import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# PDF text extraction
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class GroqResumeAnalyzer:
    """Resume analysis using Groq AI (FREE tier)"""
    
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        # Get API key from environment or settings
        self.api_key = os.environ.get('GROQ_API_KEY', getattr(settings, 'GROQ_API_KEY', ''))
    
    def analyze_resume(self, resume_text: str, job_description: str = None) -> dict:
        """
        Analyze resume using Groq's Llama 3.3 model
        Returns detailed ATS analysis with suggestions
        """
        
        if not self.api_key:
            return self._get_error_response("GROQ_API_KEY not configured")
        
        system_prompt = """You are an expert HR professional and ATS (Applicant Tracking System) specialist.
Analyze the resume and provide detailed feedback in JSON format.

IMPORTANT: Return ONLY valid JSON, no additional text.

JSON Structure:
{
    "overall_score": 85,
    "ats_score": 80,
    "sections": {
        "formatting": {
            "score": 90,
            "status": "good",
            "feedback": "Your resume has clean formatting...",
            "suggestions": ["Use consistent bullet points", "Keep margins uniform"]
        },
        "keywords": {
            "score": 75,
            "status": "warning", 
            "feedback": "Good keyword density but can be improved...",
            "suggestions": ["Add more technical keywords", "Include industry terms"],
            "found_keywords": ["Python", "JavaScript", "React"],
            "missing_keywords": ["Docker", "AWS", "CI/CD"]
        },
        "contact": {
            "score": 95,
            "status": "good",
            "feedback": "Contact information is complete...",
            "suggestions": []
        },
        "experience": {
            "score": 70,
            "status": "warning",
            "feedback": "Experience section needs improvement...",
            "suggestions": ["Add quantifiable achievements", "Use action verbs"]
        },
        "education": {
            "score": 85,
            "status": "good",
            "feedback": "Education section is well structured...",
            "suggestions": []
        },
        "skills": {
            "score": 80,
            "status": "good",
            "feedback": "Good skills section...",
            "suggestions": ["Organize skills by category"],
            "detected_skills": ["Python", "Django", "SQL"]
        }
    },
    "strengths": [
        "Clear professional summary",
        "Relevant technical skills"
    ],
    "improvements": [
        "Add more quantifiable achievements",
        "Include more industry keywords"
    ],
    "summary": "Your resume scores well overall but needs improvements in..."
}

Status values: "good" (score >= 80), "warning" (score 60-79), "error" (score < 60)"""

        user_prompt = f"""Analyze this resume for ATS compatibility and provide detailed feedback:

RESUME TEXT:
{resume_text}

{f'TARGET JOB DESCRIPTION: {job_description}' if job_description else ''}

Provide your analysis in the exact JSON format specified. Be specific and helpful."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                return self._get_error_response(f"Groq API error: {error_detail}")
            
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                analysis = json.loads(ai_content)
                return {
                    'success': True,
                    'analysis': analysis
                }
            except json.JSONDecodeError:
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', ai_content, re.DOTALL)
                if json_match:
                    analysis = json.loads(json_match.group())
                    return {
                        'success': True,
                        'analysis': analysis
                    }
                return self._get_error_response("Failed to parse AI response")
                
        except requests.exceptions.Timeout:
            return self._get_error_response("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            return self._get_error_response(f"Network error: {str(e)}")
        except Exception as e:
            return self._get_error_response(f"Analysis error: {str(e)}")
    
    def _get_error_response(self, error_message: str) -> dict:
        """Return error response with fallback analysis"""
        return {
            'success': False,
            'error': error_message,
            'analysis': self._get_fallback_analysis()
        }
    
    def _get_fallback_analysis(self) -> dict:
        """Fallback analysis when AI is unavailable"""
        return {
            "overall_score": 70,
            "ats_score": 70,
            "sections": {
                "formatting": {
                    "score": 75,
                    "status": "warning",
                    "feedback": "Unable to perform detailed analysis. Please try again.",
                    "suggestions": ["Ensure clean formatting", "Use standard fonts"]
                },
                "keywords": {
                    "score": 70,
                    "status": "warning",
                    "feedback": "Keyword analysis unavailable.",
                    "suggestions": ["Include relevant industry keywords"]
                },
                "contact": {
                    "score": 80,
                    "status": "good",
                    "feedback": "Ensure contact information is complete.",
                    "suggestions": []
                },
                "experience": {
                    "score": 70,
                    "status": "warning",
                    "feedback": "Experience analysis unavailable.",
                    "suggestions": ["Add quantifiable achievements"]
                },
                "education": {
                    "score": 75,
                    "status": "warning",
                    "feedback": "Education analysis unavailable.",
                    "suggestions": []
                },
                "skills": {
                    "score": 75,
                    "status": "warning",
                    "feedback": "Skills analysis unavailable.",
                    "suggestions": ["List relevant technical skills"]
                }
            },
            "strengths": ["Resume submitted for analysis"],
            "improvements": ["AI analysis temporarily unavailable - please try again"],
            "summary": "We couldn't complete the full analysis. Please try again in a moment."
        }


def extract_text_from_pdf(pdf_file) -> str:
    """Extract text content from uploaded PDF file"""
    if not PDF_AVAILABLE:
        return ""
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return ""


class GroqResumeAnalysisView(APIView):
    """
    API endpoint for AI-powered resume analysis using Groq
    
    POST /api/ai/analyze-resume/
    
    Accepts:
    - resume_file: PDF/DOC file upload
    - resume_text: Plain text (alternative to file)
    - job_description: Optional target job description
    """
    
    permission_classes = [AllowAny]  # Allow without login for demo
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    def post(self, request):
        resume_text = ""
        job_description = request.data.get('job_description', '')
        
        # Check for file upload
        if 'resume_file' in request.FILES:
            uploaded_file = request.FILES['resume_file']
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.pdf'):
                resume_text = extract_text_from_pdf(uploaded_file)
                if not resume_text:
                    return Response({
                        'success': False,
                        'error': 'Could not extract text from PDF. Please ensure the PDF contains readable text.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            elif file_name.endswith(('.doc', '.docx')):
                # For .doc/.docx, we'd need python-docx library
                # For now, ask user to paste text
                return Response({
                    'success': False,
                    'error': 'DOC/DOCX files require additional processing. Please paste your resume text instead.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'error': 'Unsupported file format. Please upload PDF or paste resume text.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for text input
        elif 'resume_text' in request.data:
            resume_text = request.data.get('resume_text', '').strip()
        
        if not resume_text:
            return Response({
                'success': False,
                'error': 'Please upload a resume file or provide resume text.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(resume_text) < 100:
            return Response({
                'success': False,
                'error': 'Resume text is too short. Please provide complete resume content.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform AI analysis
        analyzer = GroqResumeAnalyzer()
        result = analyzer.analyze_resume(resume_text, job_description)
        
        return Response(result)


class GroqDemoAnalysisView(APIView):
    """
    Demo endpoint that analyzes a sample resume
    
    GET /api/ai/demo-analysis/
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Sample resume for demo
        sample_resume = """
RAHUL SHARMA
Software Developer
Email: rahul.sharma@email.com | Phone: +91 9876543210
LinkedIn: linkedin.com/in/rahulsharma | GitHub: github.com/rahulsharma
Location: Bangalore, India

PROFESSIONAL SUMMARY
Passionate software developer with 2 years of experience in building web applications 
using Python, Django, and React. Strong problem-solving skills and ability to work in 
agile environments. Looking for opportunities to grow in a challenging role.

EDUCATION
Bachelor of Technology in Computer Science
XYZ Engineering College, Bangalore
2018 - 2022 | CGPA: 8.5/10

WORK EXPERIENCE
Software Developer | ABC Tech Solutions, Bangalore
June 2022 - Present
- Developed and maintained web applications using Django and React
- Worked on REST APIs for mobile applications
- Participated in code reviews and team meetings
- Fixed bugs and improved application performance

Intern | StartupXYZ, Remote
January 2022 - May 2022
- Assisted in developing features for the company's main product
- Learned about agile development practices
- Created documentation for internal tools

TECHNICAL SKILLS
Languages: Python, JavaScript, HTML, CSS, SQL
Frameworks: Django, React, Bootstrap
Tools: Git, VS Code, Postman, Linux
Databases: PostgreSQL, MySQL, MongoDB

PROJECTS
E-commerce Website
- Built a full-stack e-commerce platform with Django backend and React frontend
- Implemented user authentication, product catalog, and shopping cart

Task Management App
- Created a task management application with real-time updates
- Used WebSocket for real-time notifications

CERTIFICATIONS
- AWS Cloud Practitioner (2023)
- Python for Data Science - Coursera (2022)
"""
        
        analyzer = GroqResumeAnalyzer()
        result = analyzer.analyze_resume(sample_resume)
        
        return Response(result)


class GroqJobMatchAnalyzer:
    """AI-powered job match analysis using Groq"""
    
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', getattr(settings, 'GROQ_API_KEY', ''))
    
    def analyze_match(self, profile_text: str, job_description: str) -> dict:
        """Analyze how well a profile matches a job description"""
        
        if not self.api_key:
            return self._get_error_response("GROQ_API_KEY not configured")
        
        system_prompt = """You are an expert HR recruiter and job matching specialist.
Analyze the candidate profile against the job description and provide a detailed match analysis.

IMPORTANT: Return ONLY valid JSON, no additional text.

JSON Structure:
{
    "overall_match": 85,
    "breakdown": {
        "skills_match": {
            "score": 80,
            "matched_skills": ["Python", "JavaScript", "React"],
            "missing_skills": ["Docker", "Kubernetes"],
            "feedback": "Strong technical skills, but missing some DevOps requirements"
        },
        "experience_match": {
            "score": 75,
            "feedback": "2 years experience, job requires 4+ years. Consider highlighting leadership roles."
        },
        "education_match": {
            "score": 90,
            "feedback": "Education requirements fully met with relevant degree."
        },
        "keywords_match": {
            "score": 70,
            "matched_keywords": ["REST API", "Agile", "Full Stack"],
            "missing_keywords": ["GraphQL", "CI/CD", "Microservices"],
            "feedback": "Add more industry keywords to improve ATS score"
        }
    },
    "strengths": [
        "Strong programming fundamentals",
        "Relevant project experience"
    ],
    "gaps": [
        "Less experience than required",
        "Missing cloud certifications"
    ],
    "recommendations": [
        "Highlight any leadership or mentoring experience",
        "Add Docker and Kubernetes to your skillset",
        "Consider getting AWS Developer certification"
    ],
    "interview_tips": [
        "Prepare examples of complex projects you've built",
        "Be ready to discuss your problem-solving approach"
    ],
    "summary": "Good match with room for improvement. Focus on gaining more experience with cloud technologies."
}"""

        user_prompt = f"""Analyze this job match:

CANDIDATE PROFILE:
{profile_text}

JOB DESCRIPTION:
{job_description}

Provide detailed match analysis in the exact JSON format specified."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 2000,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                return self._get_error_response(f"Groq API error: {error_detail}")
            
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            
            analysis = json.loads(ai_content)
            return {'success': True, 'analysis': analysis}
                
        except Exception as e:
            return self._get_error_response(f"Analysis error: {str(e)}")
    
    def _get_error_response(self, error_message: str) -> dict:
        return {
            'success': False,
            'error': error_message,
            'analysis': {
                "overall_match": 75,
                "breakdown": {},
                "strengths": ["Profile analyzed"],
                "gaps": ["Detailed analysis unavailable"],
                "recommendations": ["Please try again"],
                "summary": "Analysis temporarily unavailable"
            }
        }


class GroqInterviewFeedback:
    """AI-powered interview answer feedback using Groq"""
    
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    def __init__(self):
        self.api_key = os.environ.get('GROQ_API_KEY', getattr(settings, 'GROQ_API_KEY', ''))
    
    def evaluate_answer(self, question: str, answer: str, job_role: str = "Software Developer") -> dict:
        """Evaluate an interview answer and provide feedback"""
        
        if not self.api_key:
            return self._get_error_response("GROQ_API_KEY not configured")
        
        system_prompt = """You are an expert interview coach and HR professional.
Evaluate the candidate's answer to the interview question and provide constructive feedback.

IMPORTANT: Return ONLY valid JSON, no additional text.

JSON Structure:
{
    "scores": {
        "clarity": 8.5,
        "relevance": 9.0,
        "confidence": 7.5,
        "structure": 8.0,
        "overall": 8.2
    },
    "feedback": "Your answer was well-structured and relevant. You provided good examples...",
    "strengths": [
        "Clear communication",
        "Good use of specific examples"
    ],
    "improvements": [
        "Add more quantifiable results",
        "Be more concise in delivery"
    ],
    "better_answer_tips": "Consider structuring your answer using the STAR method...",
    "follow_up_questions": [
        "Can you give another example of...",
        "How did you measure the success of..."
    ]
}

Score each aspect from 1-10 where:
- 1-4: Needs significant improvement
- 5-6: Average, needs work
- 7-8: Good, minor improvements needed
- 9-10: Excellent"""

        user_prompt = f"""Evaluate this interview answer:

JOB ROLE: {job_role}

INTERVIEW QUESTION:
{question}

CANDIDATE'S ANSWER:
{answer}

Provide detailed feedback and scores in the exact JSON format specified."""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 1500,
                "temperature": 0.3,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                self.GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                error_detail = response.json().get('error', {}).get('message', 'Unknown error')
                return self._get_error_response(f"Groq API error: {error_detail}")
            
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            
            feedback = json.loads(ai_content)
            return {'success': True, 'feedback': feedback}
                
        except Exception as e:
            return self._get_error_response(f"Evaluation error: {str(e)}")
    
    def _get_error_response(self, error_message: str) -> dict:
        return {
            'success': False,
            'error': error_message,
            'feedback': {
                "scores": {"clarity": 7, "relevance": 7, "confidence": 7, "structure": 7, "overall": 7},
                "feedback": "Unable to provide detailed feedback at this time.",
                "strengths": ["Answer provided"],
                "improvements": ["Please try again for detailed feedback"]
            }
        }


class GroqJobMatchView(APIView):
    """API endpoint for AI job match analysis"""
    
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def post(self, request):
        profile_text = request.data.get('profile', '').strip()
        job_description = request.data.get('job_description', '').strip()
        
        if not profile_text or not job_description:
            return Response({
                'success': False,
                'error': 'Both profile and job description are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        analyzer = GroqJobMatchAnalyzer()
        result = analyzer.analyze_match(profile_text, job_description)
        
        return Response(result)


class GroqInterviewFeedbackView(APIView):
    """API endpoint for AI interview answer feedback"""
    
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def post(self, request):
        question = request.data.get('question', '').strip()
        answer = request.data.get('answer', '').strip()
        job_role = request.data.get('job_role', 'Software Developer')
        
        if not question or not answer:
            return Response({
                'success': False,
                'error': 'Both question and answer are required.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        evaluator = GroqInterviewFeedback()
        result = evaluator.evaluate_answer(question, answer, job_role)
        
        return Response(result)
