# Entity Relationship Diagram (ERD)
## SkillConnect - Database Design Document

---

**Institution:** D.A.V. Velankar College of Commerce, Solapur  
**Department:** BCA Department  
**Academic Year:** 2025-2026  

**Student Name:** Nijamuddin Mujawar  
**Roll Number:** 4723  
**Project Guide:** Mr. Bhavikatti S.B. (HOD)  

**Submission Date:** 30-12-2025  
**Document Type:** ERD (Entity Relationship Diagram)  
**Activity Number:** Point 4 of Project Schedule

---

## 1. Introduction

This document presents the Entity Relationship Diagram (ERD) for SkillConnect - a voice-enabled career platform for Indian students. The database consists of **6 tables** with **5 relationships**, designed using **MySQL 8.0** and follows **3NF normalization**.

---

## 2. Database Tables

| # | Table Name | Type | Primary Key | Foreign Key | Purpose |
|---|------------|------|-------------|-------------|---------|
| 1 | **CustomUser** | Master | id | - | User accounts and profiles |
| 2 | **WorkExperience** | Child | id | user_id | Work history records |
| 3 | **Education** | Child | id | user_id | Educational qualifications |
| 4 | **Skill** | Child | id | user_id | User skills (level 1-5) |
| 5 | **Job** | Master | id | - | Job postings |
| 6 | **Application** | Junction | id | user_id, job_id | Job applications |

**Key Fields Summary:**

**CustomUser:** id, username, email, password, first_name, last_name, phone_number, profile_picture, resume_file, is_active

**WorkExperience:** id, user_id (FK), title, company, location, start_date, end_date, is_current

**Education:** id, user_id (FK), degree, school, start_year, end_year, grade

**Skill:** id, user_id (FK), name, level (1-5), created_at

**Job:** id, title, company, location, category, job_type, min_salary, max_salary, posted_date, is_active

**Application:** id, user_id (FK), job_id (FK), applied_date, status, cover_letter

---

## 3. Entity Relationship Diagram

### 3.1 Text-Based ERD (Class Diagram Style)

```
┌─────────────────────────┐                ┌─────────────────────────┐
│    WorkExperience       │                │      CustomUser         │
├─────────────────────────┤       1        ├─────────────────────────┤
│ PK  id                  │◄───────────────│ PK  id                  │
│ FK  user_id             │       n        │     username            │
│     title               │                │     email               │
│     company             │                │     password            │
│     location            │                │     first_name          │
│     start_date          │                │     last_name           │
│     end_date            │                │     phone_number        │
│     is_current          │                │     profile_score       │
└─────────────────────────┘                │     is_active           │
                                           └─────────────────────────┘
┌─────────────────────────┐                          │
│       Education         │                          │ 1
├─────────────────────────┤                          │
│ PK  id                  │◄─────────────────────────┘
│ FK  user_id             │              n
│     degree              │
│     school              │                ┌─────────────────────────┐
│     start_year          │                │         Skill           │
│     end_year            │                ├─────────────────────────┤
│     is_current          │       1        │ PK  id                  │
│     grade               │◄───────────────│ FK  user_id             │
└─────────────────────────┘       n        │     name                │
                                           │     level               │
                                           └─────────────────────────┘
┌─────────────────────────┐
│      Application        │                ┌─────────────────────────┐
├─────────────────────────┤       1        │          Job            │
│ PK  id                  │───────────────►│ PK  id                  │
│ FK  user_id             │       n        │     title               │
│ FK  job_id              │                │     company             │
│     full_name           │                │     location            │
│     email               │                │     category            │
│     phone               │                │     job_type            │
│     resume              │                │     salary_display      │
│     status              │                │     description         │
└─────────────────────────┘                │     is_active           │
        ▲                                  └─────────────────────────┘
        │ n
        │
        │ 1
        │
┌───────┴─────────────────┐
│      CustomUser         │
│  (From above)           │
└─────────────────────────┘
```

**Legend:**
- **PK** = Primary Key
- **FK** = Foreign Key
- **1** = One (Parent side)
- **n** = Many (Child side)
- **◄───** = One-to-Many Relationship
- **───►** = References/Points to

### 3.2 Visual ERD (PowerPoint Diagram)

**[INSERT POWERPOINT ERD DIAGRAM IMAGE HERE]**

> **Instructions for Document Preparation:**
> 1. Open PowerPoint ERD diagram
> 2. Save slide as PNG (File → Save As → PNG format)
> 3. Insert image here in Word document
> 4. Set image size: Full page width (16-18 cm)
> 5. Center align the image
> 6. Keep the caption below

**Figure 3.1:** SkillConnect Database - Entity Relationship Diagram  
*Visual representation showing 6 entities (CustomUser, WorkExperience, Education, Skill, Job, Application) with their attributes and relationships. Master tables shown in Blue, Child tables in Green, Junction table in Orange.*

---

### 3.3 ERD Component Summary

**Entities (6 Tables):**
- **CustomUser** (Master - Blue) - User accounts and profiles
- **WorkExperience** (Child - Green) - Work history records
- **Education** (Child - Green) - Educational qualifications
- **Skill** (Child - Green) - User skills with proficiency levels
- **Job** (Master - Blue) - Job postings from companies
- **Application** (Junction - Orange) - Bridge table connecting users and jobs

**Relationships (5 Connections):**
1. CustomUser **HAS** WorkExperience (1:Many)
2. CustomUser **HAS** Education (1:Many)
3. CustomUser **HAS** Skill (1:Many)
4. CustomUser **CREATES** Application (1:Many)
5. Job **RECEIVES** Application (1:Many)

**Legend:**
- **PK** = Primary Key (Unique identifier)
- **FK** = Foreign Key (Reference to another table)
- **UK** = Unique Key (Must be unique across records)
- **1:M** = One-to-Many Relationship
- **M:M** = Many-to-Many Relationship (via Application bridge table)

---

## 4. Relationships Analysis

**Relationship 1: CustomUser → WorkExperience**
- **Type:** One-to-Many (1:M)
- **Cardinality:** 1 User can have 0 or Many Work Experiences
- **Foreign Key:** `user_id` in WorkExperience references `id` in CustomUser
- **Business Rule:** User can add multiple work experiences to build career history
- **Example:** User "Nijamuddin" has 3 work experiences

**Relationship 2: CustomUser → Education**
- **Type:** One-to-Many (1:M)
- **Cardinality:** 1 User can have 0 or Many Education records
- **Foreign Key:** `user_id` in Education references `id` in CustomUser
- **Business Rule:** User can add multiple degrees and qualifications
- **Example:** User has BCA (2022), HSC (2019), SSC (2017)

**Relationship 3: CustomUser → Skill**
- **Type:** One-to-Many (1:M)
- **Cardinality:** 1 User can have 0 or Many Skills
- **Foreign Key:** `user_id` in Skill references `id` in CustomUser
- **Constraint:** Unique together (`user_id`, `name`) - No duplicate skills per user
- **Business Rule:** User can showcase multiple technical and soft skills
- **Example:** User has skills: Python (Expert), Django (Advanced), React (Intermediate)

**Relationship 4: CustomUser → Application**
- **Type:** One-to-Many (1:M)
- **Cardinality:** 1 User can have 0 or Many Applications
- **Foreign Key:** `user_id` in Application references `id` in CustomUser
- **Business Rule:** User can apply to multiple jobs
- **Example:** User applied to 5 different jobs

**Relationship 5: Job → Application**
- **Type:** One-to-Many (1:M)
- **Cardinality:** 1 Job can have 0 or Many Applications
- **Foreign Key:** `job_id` in Application references `id` in Job
- **Business Rule:** One job posting can receive multiple applications from different users
- **Example:** "Python Developer" job has 25 applications

### 4.6 Many-to-Many Relationship (Indirect)

**Entities Involved:** CustomUser ↔ Job  
**Bridge Table:** Application  
**How It Works:**
- One User can apply to Many Jobs
- One Job can receive applications from Many Users
- Application table contains both foreign keys: `user_id` and `job_id`
- This creates a Many-to-Many relationship through the bridge table

---

## 5. ERD Notation Standards

The ERD diagram follows industry-standard notation conventions:

### 5.1 Entity Representation

**Rectangles with Rounded Corners:**
- Represent database tables/entities
- Color-coded for clarity:
  - **Blue** = Master/Parent tables (independent entities)
  - **Green** = Child tables (dependent on parent)
  - **Orange** = Junction/Bridge tables (connect multiple entities)

### 5.2 Attribute Representation

**Ovals connected to entities:**
- Each oval represents a field/column in the table
- **Underlined attributes** = Primary Keys
- **Regular attributes** = Data fields
- Connected by lines to parent entity

### 5.3 Relationship Representation

**Diamonds between entities:**
- Diamond shape indicates relationship type
- Contains relationship name (Has, Creates, Receives, AppliesTo)
- Connected by lines showing cardinality

### 5.4 Cardinality Notation

**Numbers on relationship lines:**
- **1** = Exactly one (One side of relationship)
- **n** = Many (Multiple records allowed)
- **1:n** = One-to-Many relationship
- **n:m** = Many-to-Many relationship (requires junction table)

**Examples in SkillConnect:**
- CustomUser (1) → WorkExperience (n): One user can have multiple work experiences
- CustomUser (1) → Application (n) ← Job (1): Creates Many-to-Many via bridge table

---

## 6. Database Normalization

The SkillConnect database follows Third Normal Form (3NF) principles to ensure data integrity and minimize redundancy.

### 6.1 Normal Forms Applied:

**First Normal Form (1NF):**
✅ All tables have primary keys  
✅ No repeating groups  
✅ Atomic values in each field

**Second Normal Form (2NF):**
✅ Meets 1NF requirements  
✅ No partial dependencies  
✅ All attributes depend on entire primary key

**Third Normal Form (3NF):**
✅ Meets 2NF requirements  
✅ No transitive dependencies  
✅ All attributes depend only on primary key

### 6.2 Benefits of Normalization

✅ **Eliminates Data Redundancy** - No repeated information across tables  
✅ **Ensures Data Integrity** - Referential integrity through foreign keys  
✅ **Reduces Storage Space** - Efficient data organization  
✅ **Simplifies Updates** - Changes required in only one place  
✅ **Prevents Anomalies** - No insertion, update, or deletion anomalies

---

## 7. Indexing Strategy

### 7.1 Primary Key Indexes
All tables use auto-increment integer `id` as Primary Key for:
- Fast row identification
- Efficient joins between tables
- Guaranteed uniqueness

### 7.2 Foreign Key Indexes
Foreign keys are indexed for optimal query performance:
- `user_id` in WorkExperience, Education, Skill, Application tables
- `job_id` in Application table

### 7.3 Unique Indexes
- `email` in CustomUser - Prevents duplicate accounts
- Composite (`user_id`, `name`) in Skill - Prevents duplicate skills per user

---

| # | From → To | Type | Cardinality | Description |
|---|-----------|------|-------------|-------------|
| 1 | CustomUser → WorkExperience | 1:M | 1 to Many | One user has multiple work experiences |
| 2 | CustomUser → Education | 1:M | 1 to Many | One user has multiple education records |
| 3 | CustomUser → Skill | 1:M | 1 to Many | One user has multiple skills |
| 4 | CustomUser → Application | 1:M | 1 to Many | One user creates multiple applications |
| 5 | Job → Application | 1:M | 1 to Many | One job receives multiple applications |

**Many-to-Many Relationship:**  
CustomUser ↔ Job (via Application bridge table) - Users can apply to multiple jobs, and jobs receive applications from multiple users.

---

## 5. Database Design Features

**Normalization:** 3NF (Third Normal Form)
- Eliminates data redundancy
- Ensures data integrity through foreign key constraints
- Prevents insertion, update, and deletion anomalies

**Indexing Strategy:**
- Primary Keys: All tables use auto-increment `id`
- Foreign Keys: Indexed for optimal join performance
- Unique Keys: `email` in CustomUser, `(user_id, name)` in Skill

**Performance:**
- Total Records: 245+
- Database Size: ~15 MB
- Query Response Time: <100m6. Conclusion

The SkillConnect ERD provides a well-structured, normalized database design with 6 tables and 5 relationships. The design ensures data integrity, scalability, and optimal performance for a voice-enabled career platform serving Indian students