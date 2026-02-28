// NO LOADING SCREEN - Direct content display
// Initialize everything immediately when DOM loads
document.addEventListener('DOMContentLoaded', function() {
  console.log('🚀 SkillConnect loading - No loading screen');
  
  // Initialize AOS if available
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 800,
      offset: 50,
      once: true,
      disable: false
    });
    console.log('✅ AOS initialized');
  }
  
  // Initialize all components immediately
  initializeSearch();
  initializeNewsletter();
  initializeContactForm();
  initializeFAQ();
  initializeTestimonials();
  
  // Load dynamic content immediately
  loadStats();
  
  console.log('✅ SkillConnect initialized successfully - Fast load!');
});

// Dynamic navigation based on login status (immediate)
const jobsLink = document.getElementById('jobs-link');
const profileLink = document.getElementById('profile-link');
const companiesLink = document.getElementById('companies-link');
const resourcesLink = document.getElementById('resources-link');

// Debug navigation links
console.log('Navigation Links Found:', {
  jobs: !!jobsLink,
  profile: !!profileLink,
  companies: !!companiesLink,
  resources: !!resourcesLink
});

// Ensure companies and resources links work properly
if (companiesLink) {
  companiesLink.addEventListener('click', function(e) {
    console.log('Companies link clicked!');
    // Allow default navigation
  });
}

if (resourcesLink) {
  resourcesLink.addEventListener('click', function(e) {
    console.log('Resources link clicked!');
    // Allow default navigation
  });
}

// For testing purposes, allow direct access to profile page
// Remove this when implementing real authentication
const currentPath = window.location.pathname;
const isProfilePage = currentPath.includes('profile.html');

if (!localStorage.getItem('access_token') && !isProfilePage) {
  if (jobsLink) jobsLink.setAttribute('href', 'login.html?next=jobs.html');
  if (profileLink) profileLink.setAttribute('href', 'login.html?next=profile.html');
} else {
  if (jobsLink) jobsLink.setAttribute('href', 'jobs.html');
  if (profileLink) profileLink.setAttribute('href', 'profile.html');
  
  // Set a demo access token for profile page testing
  if (isProfilePage && !localStorage.getItem('access_token')) {
    localStorage.setItem('access_token', 'demo-token');
    localStorage.setItem('user_email', 'demo@skillconnect.com');
    localStorage.setItem('user_data', JSON.stringify({
      firstName: 'John',
      lastName: 'Doe',
      phone: '+91 9876543210'
    }));
  }
}

// Search functionality
function initializeSearch() {
  const searchBtn = document.getElementById('search-btn');
  if (searchBtn) {
    searchBtn.addEventListener('click', performSearch);
  }
}

function performSearch() {
  const keyword = document.getElementById('search-keyword')?.value.trim().toLowerCase() || '';
  const location = document.getElementById('search-location')?.value.toLowerCase() || '';
  const category = document.getElementById('search-category')?.value.toLowerCase() || '';
  const resultsDiv = document.getElementById('search-results');
  
  if (!keyword && !location && !category) {
    showNotification('Please enter search criteria', 'warning');
    return;
  }
  
  if (resultsDiv) {
    resultsDiv.innerHTML = '<div class="loading">🔍 Searching for jobs...</div>';
    resultsDiv.classList.add('show');
    
    // Simulate search with sample data
    setTimeout(() => {
      displaySampleSearchResults(resultsDiv, keyword, location, category);
    }, 1500);
  }
}

// Display sample search results
function displaySampleSearchResults(container, keyword, location, category) {
  const sampleJobs = [
    {
      title: 'React Developer',
      company: 'Tech Innovations Pvt Ltd',
      location: 'Mumbai',
      type: 'Full-time',
      description: 'Looking for experienced React developer with 2+ years in modern JavaScript frameworks and API integration.'
    },
    {
      title: 'UI/UX Designer',
      company: 'Creative Digital Studio',
      location: 'Bangalore',
      type: 'Full-time',
      description: 'Seeking talented designer proficient in Figma, Adobe XD, and user research methodologies.'
    },
    {
      title: 'Data Analyst',
      company: 'Analytics Solutions Corp',
      location: 'Pune',
      type: 'Full-time',
      description: 'Join our analytics team to work with big data, create insights, and drive business decisions.'
    },
    {
      title: 'Product Manager',
      company: 'Startup Hub India',
      location: 'Delhi',
      type: 'Full-time',
      description: 'Lead product strategy and development in fast-paced startup environment with growth opportunities.'
    }
  ];
  
  // Filter based on search criteria
  const filteredJobs = sampleJobs.filter(job => {
    let matches = true;
    if (keyword && !job.title.toLowerCase().includes(keyword) && !job.description.toLowerCase().includes(keyword)) {
      matches = false;
    }
    if (location && job.location.toLowerCase() !== location) {
      matches = false;
    }
    if (category) {
      const categoryMap = {
        'it': ['react', 'developer', 'analyst'],
        'design': ['designer', 'ui', 'ux'],
        'marketing': ['marketing', 'manager'],
        'finance': ['finance', 'analyst']
      };
      if (categoryMap[category] && !categoryMap[category].some(term => 
        job.title.toLowerCase().includes(term) || job.description.toLowerCase().includes(term))) {
        matches = false;
      }
    }
    return matches;
  });
  
  if (filteredJobs.length === 0) {
    container.innerHTML = '<div class="no-results">❌ No jobs found. Try different criteria.</div>';
    return;
  }
  
  const jobsHTML = filteredJobs.map(job => `
    <div class="search-result-item">
      <h4>${job.title}</h4>
      <div class="company">${job.company}</div>
      <div class="job-meta">
        <span class="location">📍 ${job.location}</span>
        <span class="job-type">💼 ${job.type}</span>
      </div>
      <p>${job.description}</p>
      <button class="btn-apply-search" onclick="applyToJob('${job.title}', '${job.company}')">Apply Now</button>
    </div>
  `).join('');
  
  container.innerHTML = jobsHTML;
}

// Quick search function
function quickSearch(term) {
  const searchInput = document.getElementById('search-keyword');
  if (searchInput) {
    searchInput.value = term;
    performSearch();
  }
}

// Search by category
function searchByCategory(category) {
  // Store category in sessionStorage for the jobs page
  sessionStorage.setItem('selectedCategory', category);
  
  // Redirect to jobs page
  window.location.href = 'jobs.html';
}

// Newsletter functionality
function initializeNewsletter() {
  const subscribeBtn = document.getElementById('subscribe-btn');
  const newsletterEmail = document.getElementById('newsletter-email');
  
  if (subscribeBtn) {
    subscribeBtn.addEventListener('click', subscribeToNewsletter);
  }
  
  if (newsletterEmail) {
    newsletterEmail.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        subscribeToNewsletter();
      }
    });
  }
}

function subscribeToNewsletter() {
  const emailInput = document.getElementById('newsletter-email');
  const subscribeBtn = document.getElementById('subscribe-btn');
  
  if (!emailInput || !subscribeBtn) return;
  
  const email = emailInput.value.trim();
  
  if (!email) {
    showNotification('Please enter your email address', 'warning');
    return;
  }
  
  if (!isValidEmail(email)) {
    showNotification('Please enter a valid email address', 'error');
    return;
  }
  
  // Show loading state
  const originalText = subscribeBtn.innerHTML;
  subscribeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
  subscribeBtn.disabled = true;
  
  // Simulate API call
  setTimeout(() => {
    showNotification('🎉 Successfully subscribed to newsletter!', 'success');
    emailInput.value = '';
    subscribeBtn.innerHTML = originalText;
    subscribeBtn.disabled = false;
  }, 2000);
}

// Contact form functionality
function initializeContactForm() {
  const contactForm = document.getElementById('contact-form');
  
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const name = document.getElementById('contact-name')?.value.trim();
      const email = document.getElementById('contact-email')?.value.trim();
      const message = document.getElementById('contact-message')?.value.trim();
      
      if (!name || !email || !message) {
        showNotification('Please fill in all fields', 'warning');
        return;
      }
      
      if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
      }
      
      // Show loading state
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
          showNotification('✅ Message sent successfully!', 'success');
          contactForm.reset();
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }, 2000);
      }
    });
  }
}

// Load statistics with animation
function loadStats() {
  console.log('🔢 Loading stats animation...');
  
  // Start animation immediately
  setTimeout(() => {
    const statNumbers = document.querySelectorAll('.stat-number');
    console.log('Found stat elements:', statNumbers.length);
    
    statNumbers.forEach((stat, index) => {
      const target = parseInt(stat.getAttribute('data-count')) || 0;
      console.log(`Animating stat ${index + 1}: ${target}`);
      
      let current = 0;
      const increment = target / 100; // 100 steps
      const delay = 20; // 20ms per step = 2 second total
      
      const animate = () => {
        current += increment;
        if (current >= target) {
          stat.textContent = target.toLocaleString();
          console.log(`Stat ${index + 1} completed: ${target}`);
        } else {
          stat.textContent = Math.floor(current).toLocaleString();
          setTimeout(animate, delay);
        }
      };
      
      // Start each animation with a small delay
      setTimeout(animate, index * 200);
    });
  }, 1000);
}

// Format large numbers (utility function)
function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

// Load recent jobs with sample data
function loadRecentJobs() {
  console.log('🔍 Loading recent jobs...');
  const jobsGrid = document.getElementById('recent-jobs-grid');
  const jobsLoading = document.getElementById('jobs-loading');
  const jobsError = document.getElementById('jobs-error');
  
  console.log('Elements found:', {
    jobsGrid: !!jobsGrid,
    jobsLoading: !!jobsLoading,
    jobsError: !!jobsError
  });
  
  if (!jobsGrid) {
    console.error('❌ Jobs grid element not found!');
    return;
  }
  
  // Hide loading immediately
  if (jobsLoading) jobsLoading.style.display = 'none';
  if (jobsError) jobsError.style.display = 'none';
  
  // Load sample data immediately - no delay
  try {
    const sampleJobs = [
      {
        title: 'Senior Full Stack Developer',
        company: 'TechCorp Solutions',
        location: 'Mumbai',
        type: 'Full-time',
        description: 'Join our engineering team to build scalable web applications using React, Node.js, and cloud technologies.',
        salary: '12-18 LPA'
      },
      {
        title: 'Creative UI/UX Designer',
        company: 'Design Studio Pro',
        location: 'Bangalore',
        type: 'Full-time',
        description: 'Create amazing user experiences for mobile and web apps using modern design principles and tools.',
        salary: '8-12 LPA'
      },
      {
        title: 'Data Science Specialist',
        company: 'Analytics Hub India',
        location: 'Pune',
        type: 'Full-time',
        description: 'Work with big data, machine learning models, and AI to drive business insights and decisions.',
        salary: '15-22 LPA'
      },
      {
        title: 'Digital Marketing Manager',
        company: 'Growth Marketing Co',
        location: 'Delhi',
        type: 'Full-time',
        description: 'Lead digital marketing campaigns, SEO strategies, and social media growth for multiple brands.',
        salary: '10-15 LPA'
      }
    ];
    
    const jobsHTML = sampleJobs.map(job => `
      <div class="job-card" data-aos="fade-up">
        <div class="job-header">
          <div>
            <h3>${job.title}</h3>
            <div class="company">${job.company}</div>
          </div>
          <div class="job-type">${job.type}</div>
        </div>
        <div class="job-meta">
          <span><i class="fas fa-map-marker-alt"></i> ${job.location}</span>
          <span><i class="fas fa-clock"></i> Posted recently</span>
        </div>
        <p>${job.description}</p>
        <div class="job-footer">
          <div class="job-salary">₹${job.salary}</div>
          <button class="btn-apply" onclick="applyToJob('${job.title}', '${job.company}')">Apply Now</button>
        </div>
      </div>
    `).join('');
    
    jobsGrid.innerHTML = jobsHTML;
    console.log('✅ Jobs loaded successfully:', sampleJobs.length, 'jobs');
    
    // Re-initialize AOS for new elements
    if (typeof AOS !== 'undefined') {
      AOS.refresh();
      console.log('✅ AOS refreshed');
    }
    
  } catch (error) {
    console.error('❌ Error loading jobs:', error);
    if (jobsLoading) jobsLoading.style.display = 'none';
    if (jobsError) jobsError.style.display = 'block';
  }
}

// Apply to job function
function applyToJob(title, company) {
  const token = localStorage.getItem('access_token');
  if (!token) {
    showNotification('Please login to apply for jobs', 'warning');
    setTimeout(() => {
      window.location.href = 'login.html?next=' + encodeURIComponent(window.location.pathname);
    }, 2000);
    return;
  }
  
  showNotification(`🎯 Application submitted for ${title} at ${company}!`, 'success');
}

// FAQ functionality
function initializeFAQ() {
  const faqQuestions = document.querySelectorAll('.faq-question');
  
  faqQuestions.forEach(question => {
    question.addEventListener('click', function() {
      toggleFaq(this);
    });
  });
}

function toggleFaq(element) {
  const faqItem = element.closest('.faq-item');
  const isActive = faqItem.classList.contains('active');
  
  // Close all other FAQ items
  document.querySelectorAll('.faq-item').forEach(item => {
    item.classList.remove('active');
  });
  
  // Toggle current item
  if (!isActive) {
    faqItem.classList.add('active');
  }
}

// Testimonials functionality
let currentTestimonial = 0;
const testimonials = [];

function initializeTestimonials() {
  const testimonialCards = document.querySelectorAll('.testimonial-card');
  const dots = document.querySelectorAll('.dot');
  
  testimonialCards.forEach((card, index) => {
    testimonials.push(card);
    if (index !== 0) {
      card.classList.remove('active');
    }
  });
  
  // Auto-rotate testimonials every 5 seconds
  if (testimonials.length > 1) {
    setInterval(nextTestimonial, 5000);
  }
}

function nextTestimonial() {
  if (testimonials.length === 0) return;
  
  testimonials[currentTestimonial]?.classList.remove('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.remove('active');
  
  currentTestimonial = (currentTestimonial + 1) % testimonials.length;
  
  testimonials[currentTestimonial]?.classList.add('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.add('active');
}

function previousTestimonial() {
  if (testimonials.length === 0) return;
  
  testimonials[currentTestimonial]?.classList.remove('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.remove('active');
  
  currentTestimonial = currentTestimonial === 0 ? testimonials.length - 1 : currentTestimonial - 1;
  
  testimonials[currentTestimonial]?.classList.add('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.add('active');
}

function goToTestimonial(index) {
  if (testimonials.length === 0 || index >= testimonials.length) return;
  
  testimonials[currentTestimonial]?.classList.remove('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.remove('active');
  
  currentTestimonial = index;
  
  testimonials[currentTestimonial]?.classList.add('active');
  document.querySelectorAll('.dot')[currentTestimonial]?.classList.add('active');
}

// Utility functions
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function formatNumber(num) {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K';
  }
  return num.toString();
}

function showNotification(message, type = 'info') {
  // Remove existing notifications
  const existingNotifications = document.querySelectorAll('.notification');
  existingNotifications.forEach(notification => {
    notification.remove();
  });
  
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <div class="notification-content">
      <span>${message}</span>
    </div>
    <button class="notification-close" onclick="this.parentElement.remove()">
      <i class="fas fa-times"></i>
    </button>
  `;
  
  // Style the notification
  Object.assign(notification.style, {
    position: 'fixed',
    top: '20px',
    right: '20px',
    padding: '16px 20px',
    borderRadius: '12px',
    color: 'white',
    fontWeight: '600',
    zIndex: '9999',
    transform: 'translateX(100%)',
    transition: 'all 0.3s ease',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: '12px',
    minWidth: '300px',
    maxWidth: '400px',
    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)'
  });
  
  // Set background color based on type
  const colors = {
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6'
  };
  notification.style.backgroundColor = colors[type] || colors.info;
  
  // Add to DOM
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);
  
  // Remove after 5 seconds
  setTimeout(() => {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
      if (notification.parentElement) {
        notification.remove();
      }
    }, 300);
  }, 5000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Back to top functionality
const backToTopBtn = document.getElementById('back-to-top');
if (backToTopBtn) {
  window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
      backToTopBtn.classList.add('show');
    } else {
      backToTopBtn.classList.remove('show');
    }
  });
  
  backToTopBtn.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Navbar scroll effect
window.addEventListener('scroll', function() {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    if (window.scrollY > 100) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

console.log('🚀 SkillConnect Premium UI loaded successfully! Welcome NijaMujawar!');

// Missing functions implementation
function quickSearch(query) {
  document.getElementById('search-keyword').value = query;
  performSearch();
}

function searchByCategory(category) {
  document.getElementById('search-category').value = category;
  performSearch();
}

function toggleBookmark(jobId) {
  showNotification('Job bookmarked successfully!', 'success');
}

function applyToJob(jobId) {
  // Check if user is logged in
  if (!localStorage.getItem('access_token')) {
    showNotification('Please login to apply for jobs', 'warning');
    setTimeout(() => {
      window.location.href = 'login.html';
    }, 2000);
  } else {
    showNotification('Application submitted successfully!', 'success');
  }
}

// Initialize Newsletter
function initializeNewsletter() {
  const subscribeBtn = document.getElementById('subscribe-btn');
  if (subscribeBtn) {
    subscribeBtn.addEventListener('click', handleNewsletterSubscribe);
  }
}

function handleNewsletterSubscribe() {
  const emailInput = document.getElementById('newsletter-email');
  const email = emailInput.value.trim();
  const btnText = document.querySelector('.btn-text');
  const btnLoading = document.querySelector('.btn-loading');
  
  if (!email) {
    showNotification('Please enter your email address', 'warning');
    return;
  }
  
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    showNotification('Please enter a valid email address', 'error');
    return;
  }
  
  // Show loading
  btnText.style.display = 'none';
  btnLoading.style.display = 'inline-block';
  
  // Simulate API call
  setTimeout(() => {
    btnText.style.display = 'inline-block';
    btnLoading.style.display = 'none';
    emailInput.value = '';
    showNotification('Successfully subscribed to newsletter!', 'success');
  }, 2000);
}

// Initialize Contact Form
function initializeContactForm() {
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', handleContactForm);
  }
}

function handleContactForm(e) {
  e.preventDefault();
  
  const name = document.getElementById('contact-name').value.trim();
  const email = document.getElementById('contact-email').value.trim();
  const message = document.getElementById('contact-message').value.trim();
  
  if (!name || !email || !message) {
    showNotification('Please fill in all fields', 'warning');
    return;
  }
  
  // Simulate form submission
  showNotification('Message sent successfully!', 'success');
  e.target.reset();
}

// Initialize FAQ
function initializeFAQ() {
  // FAQ functionality already implemented globally
}

function toggleFaq(element) {
  const faqItem = element.parentElement;
  const answer = faqItem.querySelector('.faq-answer');
  const icon = element.querySelector('.faq-icon');
  
  // Close other FAQs
  document.querySelectorAll('.faq-item').forEach(item => {
    if (item !== faqItem) {
      item.classList.remove('active');
      item.querySelector('.faq-answer').style.maxHeight = '0';
      item.querySelector('.faq-icon').style.transform = 'rotate(0deg)';
    }
  });
  
  // Toggle current FAQ
  faqItem.classList.toggle('active');
  
  if (faqItem.classList.contains('active')) {
    answer.style.maxHeight = answer.scrollHeight + 'px';
    icon.style.transform = 'rotate(45deg)';
  } else {
    answer.style.maxHeight = '0';
    icon.style.transform = 'rotate(0deg)';
  }
}

// Initialize Testimonials
function initializeTestimonials() {
  // Testimonial functionality already implemented
}

let currentTestimonialIndex = 0;

function nextTestimonial() {
  const testimonials = document.querySelectorAll('.testimonial-card');
  const dots = document.querySelectorAll('.dot');
  
  testimonials[currentTestimonialIndex].classList.remove('active');
  dots[currentTestimonialIndex].classList.remove('active');
  
  currentTestimonialIndex = (currentTestimonialIndex + 1) % testimonials.length;
  
  testimonials[currentTestimonialIndex].classList.add('active');
  dots[currentTestimonialIndex].classList.add('active');
}

function previousTestimonial() {
  const testimonials = document.querySelectorAll('.testimonial-card');
  const dots = document.querySelectorAll('.dot');
  
  testimonials[currentTestimonialIndex].classList.remove('active');
  dots[currentTestimonialIndex].classList.remove('active');
  
  currentTestimonialIndex = (currentTestimonialIndex - 1 + testimonials.length) % testimonials.length;
  
  testimonials[currentTestimonialIndex].classList.add('active');
  dots[currentTestimonialIndex].classList.add('active');
}

function currentTestimonial(index) {
  const testimonials = document.querySelectorAll('.testimonial-card');
  const dots = document.querySelectorAll('.dot');
  
  testimonials[currentTestimonialIndex].classList.remove('active');
  dots[currentTestimonialIndex].classList.remove('active');
  
  currentTestimonialIndex = index;
  
  testimonials[currentTestimonialIndex].classList.add('active');
  dots[currentTestimonialIndex].classList.add('active');
}

// Mobile Menu Toggle
const mobileToggle = document.getElementById('mobile-toggle');
const navLinks = document.getElementById('nav-links');

if (mobileToggle && navLinks) {
  mobileToggle.addEventListener('click', function() {
    navLinks.classList.toggle('active');
    mobileToggle.classList.toggle('active');
  });
}