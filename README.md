# SkillConnect - Professional Career Platform

![SkillConnect Logo](https://img.shields.io/badge/SkillConnect-Career%20Platform-blue?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)

> **India's comprehensive career development platform** - combining job search, professional tools, and career guidance in one place.

---

## 🎯 Project Overview

**SkillConnect** is a full-stack web application designed to help students and professionals with:
- 🔍 **Job Search & Applications** - Browse and apply to verified opportunities
- 🎤 **Voice-Based Job Search** - India's FIRST voice-enabled job portal
- 💬 **WhatsApp Job Sharing** - Share opportunities instantly via WhatsApp
- 📝 **Resume Building** - Professional CV creation tools
- 💼 **Career Tools** - 13 comprehensive career development features
- 👤 **Profile Management** - LinkedIn-style professional profiles
- 🎯 **Interview Preparation** - Practice and guidance resources

---

## 🌟 UNIQUE FEATURES (Not in LinkedIn/Naukri/Indeed)

### 1. 🎤 Voice-Based Job Search
**India's FIRST voice-enabled job portal!**
- Natural language processing
- English + Hindi support ready
- Hands-free job searching
- Browser-based (no app needed)
- **Example:** Say "Find React developer jobs in Mumbai" and search executes automatically!

**Technology:** Web Speech API (browser built-in, free)

### 2. 💬 WhatsApp Job Sharing
**Designed specifically for Indian users!**
- One-click WhatsApp job sharing
- Professional formatted messages
- Share job details with friends/family
- Perfect for mobile-first users
- **Why Unique:** 500M+ WhatsApp users in India - we make job discovery social!

### 3. 🌐 Complete Career Ecosystem
- 13 integrated career tools in one platform
- Freemium business model (7 free + 6 premium tools)
- Student-focused affordable pricing
- Mobile-responsive design

---

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.8+
- MySQL Server
- Modern web browser
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/skillconnect.git
cd skillconnect-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
```python
# Update core/settings.py with your MySQL credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillconnect_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Frontend: Open `index.html` from `skillconnect-frontend/templates/` folder
- Backend: `http://127.0.0.1:8000`
- Admin Panel: `http://127.0.0.1:8000/admin`

---

## 💻 Tech Stack

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - API development
- **MySQL** - Relational database
- **JWT Authentication** - Secure user sessions

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid/Flexbox
- **Vanilla JavaScript** - Interactive features
- **Responsive Design** - Mobile-first approach

### Tools & Libraries
- **django-cors-headers** - CORS handling
- **mysqlclient** - MySQL database adapter
- **Pillow** - Image processing

---

## 📁 Project Structure

```
skillconnect/
├── skillconnect-backend/
│   ├── core/                 # Django project settings
│   ├── accounts/             # User authentication & profiles
│   ├── jobs/                 # Job listings & applications
│   ├── newsletter/           # Newsletter & contact forms
│   ├── resumes/              # Resume management
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, images
│   ├── media/                # User uploads
│   └── manage.py
│
└── skillconnect-frontend/
    └── templates/            # Frontend HTML files
        ├── index.html        # Landing page
        ├── jobs.html         # Job listings
        ├── profile.html      # User profile
        ├── login.html        # Authentication
        └── assets/           # CSS, JS, images
```

---

## ✨ Key Features

### 🔐 Authentication System
- User registration with email verification
- Secure login with JWT tokens
- Password reset functionality
- Session management

### 💼 Job Platform
- Browse jobs with advanced filters
- Apply to positions (requires login)
- Track application status
- Save favorite jobs

### 🛠️ 13 Career Tools

**Premium Tools (Login Required):**
1. **Resume Builder** - Professional CV creation
2. **Interview Prep** - Common questions & answers
3. **Salary Calculator** - Market rate estimator
4. **Skill Development** - Learning path recommendations
5. **Career Community** - Professional networking
6. **Career Blog** - Industry insights

**Free Tools:**
7. **Tech Interview Guide** - Technical preparation
8. **ATS Templates** - Resume formats that pass screening
9. **Salary Negotiation** - Tips and strategies
10. **LinkedIn Optimization** - Profile improvement guide
11. **AI Resume Scanner** - Automated resume analysis
12. **Mock Interview AI** - Practice with AI
13. **Job Match Analyzer** - Find suitable opportunities

### 👤 User Profiles
- Work experience management
- Education history
- Skills showcase
- Profile completion tracking

---

## 🔌 API Endpoints

### Authentication
```
POST /api/accounts/register/      # User registration
POST /api/accounts/login/         # User login
GET  /api/accounts/profile/       # Get profile
PUT  /api/accounts/profile/       # Update profile
```

### Jobs
```
GET  /api/jobs/                   # List all jobs
GET  /api/jobs/<id>/              # Job details
POST /api/jobs/apply/             # Apply to job
GET  /api/jobs/applications/      # User applications
```

### Newsletter
```
POST /api/newsletter/subscribe/   # Newsletter subscription
POST /api/newsletter/contact/     # Contact form
```

---

## 📊 Database Schema

### Core Tables
- **CustomUser** - User accounts and authentication
- **WorkExperience** - User employment history
- **Education** - Academic background
- **Skills** - User competencies
- **Jobs** - Available job postings
- **JobApplications** - Application tracking

### Relationships
- One User → Many Work Experiences
- One User → Many Education Records
- One User → Many Skills
- One User → Many Job Applications
- One Job → Many Applications

---

## 🎨 Features Implemented

### ✅ Core Features
- ✅ User registration and login (JWT authentication)
- ✅ Job search with advanced filters (location, category, keyword)
- ✅ Job application system with tracking
- ✅ User profile management (CRUD operations)
- ✅ Work experience management
- ✅ Education history management
- ✅ Skills portfolio
- ✅ Newsletter subscription system
- ✅ Contact form with validation
- ✅ Category-based job exploration
- ✅ Mobile responsive design
- ✅ Admin panel for data management

### 🌟 UNIQUE Features (Market Differentiation)
- ✅ **Voice-Based Job Search** 🎤
  - Natural language voice commands
  - English + Hindi support
  - Real-time speech recognition
  - Hands-free browsing experience
  
- ✅ **WhatsApp Job Sharing** 💬
  - One-click professional job sharing
  - Auto-formatted messages with job details
  - Social job discovery
  - Mobile-optimized sharing
  
- ✅ **13 Integrated Career Tools** 🛠️
  - Complete career development ecosystem
  - Freemium model (7 free + 6 premium)
  - Resume builder, interview prep, salary calculator
  - LinkedIn optimization, skill development

### 🆕 Recent Updates (December 2025)
- ✅ Voice search integration (homepage + jobs page)
- ✅ WhatsApp share buttons on job cards
- ✅ Enhanced search functionality with voice commands
- ✅ Improved contact form API integration
- ✅ Newsletter subscription with loading states
- ✅ Delete experience/education functionality
- ✅ Purple voice search button with status indicator

---

## 🔒 Security Features

- **Password Hashing** - Django's built-in PBKDF2 algorithm
- **JWT Authentication** - Secure token-based sessions
- **CSRF Protection** - Cross-Site Request Forgery prevention
- **Input Validation** - Server-side data sanitization
- **SQL Injection Prevention** - ORM-based queries
- **File Upload Security** - Type and size validation

---

## 📱 Responsive Design

The platform is fully responsive and optimized for:
- 📱 Mobile phones (320px - 480px)
- 📱 Tablets (481px - 768px)
- 💻 Laptops (769px - 1024px)
- 🖥️ Desktops (1025px+)

---

## 🧪 Testing

### Manual Testing Completed
- ✅ User registration flow
- ✅ Login authentication
- ✅ Job application process
- ✅ Profile updates
- ✅ Search functionality
- ✅ Contact form submission
- ✅ Mobile responsiveness
- ✅ Browser compatibility (Chrome, Firefox, Edge, Safari)

---

## 🚀 Future Enhancements

### Phase 2 (Planned)
- [ ] Email notifications for job applications
- [ ] Advanced AI-powered job matching
- [ ] Company profile pages
- [ ] Real-time chat system
- [ ] Video interview integration

### Phase 3 (Long-term)
- [ ] React Native mobile app
- [ ] Machine learning recommendations
- [ ] Payment gateway integration
- [ ] Analytics dashboard
- [ ] API marketplace

---

## 📝 Documentation

Complete project documentation available in:
- `FINAL_PROJECT_DOCUMENTATION.md` - Full project report
- `PRESENTATION_DEMO_SCRIPT.md` - Live demo guide
- `PROJECT_DIAGRAMS.md` - Technical diagrams (ERD, DFD, etc.)
- `screenshots/` - Visual documentation

---

## 🎓 Academic Information

**Student:** Nijamuddin Mujawar  
**Roll No:** 4723  
**Course:** BCA  
**College:** D.A.V. Velankar College Of Commerce, Solapur  
**Academic Year:** 2025-26  
**Project Duration:** 6 weeks (August - September 2025)

---

## 👨‍💻 Developer

**Nijamuddin Mujawar**  
- 📧 Email: nijamuddinmujawar77@gmail.com
- 💼 LinkedIn: [Your LinkedIn Profile]
- 🐱 GitHub: [Your GitHub Profile]

---

## 📄 License

This project is developed for academic purposes as part of BCA final year curriculum.

---

## 🙏 Acknowledgments

- Django Documentation Team
- Stack Overflow Community
- MDN Web Docs
- MySQL Documentation
- All open-source contributors

---

## 📞 Support

For questions, issues, or feedback:
- Open an issue on GitHub
- Email: nijamuddinmujawar77@gmail.com
- Use the contact form on the website

---

**⭐ If you find this project helpful, please consider giving it a star!**

---

*Last Updated: December 7, 2025*
