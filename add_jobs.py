import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from jobs.models import Job

jobs_data = [
    {
        "title": "Frontend Developer",
        "company": "TCS",
        "location": "Mumbai, India",
        "category": "it",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "hybrid",
        "min_salary": 400000,
        "max_salary": 700000,
        "salary_display": "₹4-7 LPA",
        "description": "We are looking for a skilled Frontend Developer to join our team. You will be responsible for building user-friendly web applications using React.js and modern JavaScript.",
        "requirements": "Bachelor's degree in Computer Science or related field. Strong knowledge of HTML, CSS, JavaScript. Experience with React.js or Angular.",
        "skills": ["React.js", "JavaScript", "HTML", "CSS", "Git"],
        "company_logo": "🏢",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Python Developer",
        "company": "Infosys",
        "location": "Bangalore, India",
        "category": "it",
        "job_type": "full-time",
        "experience_level": "mid",
        "work_mode": "office",
        "min_salary": 800000,
        "max_salary": 1200000,
        "salary_display": "₹8-12 LPA",
        "description": "Join our Python development team to build scalable backend systems. Work with Django, FastAPI, and cloud technologies.",
        "requirements": "3+ years experience in Python. Knowledge of Django/Flask. Experience with REST APIs and databases.",
        "skills": ["Python", "Django", "REST API", "PostgreSQL", "AWS"],
        "company_logo": "💻",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Data Analyst",
        "company": "Wipro",
        "location": "Pune, India",
        "category": "it",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "hybrid",
        "min_salary": 500000,
        "max_salary": 800000,
        "salary_display": "₹5-8 LPA",
        "description": "Analyze large datasets to provide business insights. Create dashboards and reports using Power BI and Python.",
        "requirements": "Strong analytical skills. Knowledge of SQL, Python, Excel. Experience with data visualization tools.",
        "skills": ["Python", "SQL", "Power BI", "Excel", "Statistics"],
        "company_logo": "📊",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Digital Marketing Executive",
        "company": "Zomato",
        "location": "Gurugram, India",
        "category": "marketing",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "office",
        "min_salary": 300000,
        "max_salary": 500000,
        "salary_display": "₹3-5 LPA",
        "description": "Drive digital marketing campaigns across social media, Google Ads, and email marketing. Analyze campaign performance.",
        "requirements": "Knowledge of SEO, SEM, Social Media Marketing. Experience with Google Analytics and Facebook Ads.",
        "skills": ["SEO", "Google Ads", "Social Media", "Analytics", "Content Marketing"],
        "company_logo": "🍕",
        "company_size": "medium",
        "is_active": True
    },
    {
        "title": "Backend Developer Intern",
        "company": "SkillConnect Labs",
        "location": "Remote",
        "category": "it",
        "job_type": "internship",
        "experience_level": "entry",
        "work_mode": "remote",
        "min_salary": 10000,
        "max_salary": 20000,
        "salary_display": "₹10-20K/month",
        "description": "Learn and work on real projects. Build APIs using Django and Node.js. Great learning opportunity for freshers.",
        "requirements": "Currently pursuing or recently completed degree in CS/IT. Basic knowledge of Python or JavaScript.",
        "skills": ["Python", "Django", "Node.js", "Git", "REST API"],
        "company_logo": "🚀",
        "company_size": "startup",
        "is_active": True
    },
    {
        "title": "UI/UX Designer",
        "company": "Flipkart",
        "location": "Bangalore, India",
        "category": "design",
        "job_type": "full-time",
        "experience_level": "mid",
        "work_mode": "hybrid",
        "min_salary": 1000000,
        "max_salary": 1500000,
        "salary_display": "₹10-15 LPA",
        "description": "Design beautiful and intuitive user interfaces for our e-commerce platform. Conduct user research and usability testing.",
        "requirements": "3+ years of UI/UX experience. Proficiency in Figma, Adobe XD. Strong portfolio required.",
        "skills": ["Figma", "Adobe XD", "User Research", "Prototyping", "Design Systems"],
        "company_logo": "🛒",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "HR Executive",
        "company": "Reliance Industries",
        "location": "Mumbai, India",
        "category": "hr",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "office",
        "min_salary": 350000,
        "max_salary": 500000,
        "salary_display": "₹3.5-5 LPA",
        "description": "Handle recruitment, employee onboarding, and HR operations. Manage employee records and payroll processing.",
        "requirements": "MBA in HR or related field. Good communication skills. Knowledge of HR software.",
        "skills": ["Recruitment", "Employee Relations", "Payroll", "MS Office", "Communication"],
        "company_logo": "🏭",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Full Stack Developer",
        "company": "Amazon",
        "location": "Hyderabad, India",
        "category": "it",
        "job_type": "full-time",
        "experience_level": "senior",
        "work_mode": "hybrid",
        "min_salary": 2500000,
        "max_salary": 4000000,
        "salary_display": "₹25-40 LPA",
        "description": "Build and maintain large-scale distributed systems. Work with React, Node.js, and AWS services.",
        "requirements": "6+ years of full stack development experience. Strong problem-solving skills. Experience with microservices.",
        "skills": ["React", "Node.js", "AWS", "MongoDB", "Microservices"],
        "company_logo": "📦",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Content Writer",
        "company": "Times of India",
        "location": "Delhi, India",
        "category": "marketing",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "office",
        "min_salary": 200000,
        "max_salary": 400000,
        "salary_display": "₹2-4 LPA",
        "description": "Write engaging articles, blogs, and news content. Research trending topics and create SEO-optimized content.",
        "requirements": "Excellent writing skills in English/Hindi. Knowledge of SEO. Journalism or Mass Communication degree preferred.",
        "skills": ["Content Writing", "SEO", "Research", "Editing", "Social Media"],
        "company_logo": "📰",
        "company_size": "large",
        "is_active": True
    },
    {
        "title": "Sales Executive",
        "company": "HDFC Bank",
        "location": "Solapur, India",
        "category": "sales",
        "job_type": "full-time",
        "experience_level": "entry",
        "work_mode": "office",
        "min_salary": 250000,
        "max_salary": 400000,
        "salary_display": "₹2.5-4 LPA",
        "description": "Sell banking products like loans, credit cards, and insurance. Meet monthly sales targets and build customer relationships.",
        "requirements": "Graduate in any discipline. Good communication skills. Willingness to do field work.",
        "skills": ["Sales", "Communication", "Negotiation", "Customer Service", "Banking"],
        "company_logo": "🏦",
        "company_size": "large",
        "is_active": True
    },
]

print("Adding jobs to database...")
count = 0
for job_data in jobs_data:
    job, created = Job.objects.get_or_create(
        title=job_data["title"],
        company=job_data["company"],
        defaults=job_data
    )
    if created:
        count += 1
        print(f"✅ Added: {job.title} at {job.company}")
    else:
        print(f"⏭️ Already exists: {job.title} at {job.company}")

print(f"\n🎉 Done! {count} new jobs added. Total jobs: {Job.objects.count()}")
