# Production-Ready Job Board Platform Backend

A clean, modular, and secure RESTful API backend built with **Django 5**, **Django REST Framework (DRF)**, **Simple JWT Authentication**, **PostgreSQL**, **Celery + Redis**, and **drf-spectacular (Swagger UI)**.

---

## Tech Stack & Highlights

- **Framework**: Python 3.12+, Django 5.1+, Django REST Framework 3.14+
- **Authentication**: JWT Access & Refresh Tokens (`djangorestframework-simplejwt`) with Token Blacklisting
- **Database**: PostgreSQL (with automatic zero-friction SQLite fallback for local development)
- **Asynchronous Tasks**: Celery + Redis for asynchronous notification dispatches
- **API Documentation**: OpenAPI 3.0 / Swagger UI generated via `drf-spectacular`
- **Filtering & Search**: `django-filter` supporting location, salary range, experience, job type, skills, company name, and full-text search
- **File Validation**: Strict Resume file validation (PDF only, maximum 5MB size limit)

---

## Directory Structure

```
jobBoard/
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── config/
│   ├── settings/
│   │   └── base.py          # Unified modular settings with SQLite fallback
│   ├── urls.py               # Master API routing & Swagger docs
│   ├── celery.py             # Celery task configuration
│   ├── wsgi.py
│   └── asgi.py
└── apps/
    ├── common/               # Shared exception handlers, permissions, pagination, validators
    ├── accounts/             # Custom User model, CandidateProfile, EmployerProfile, Auth APIs
    ├── jobs/                 # Job posting, search filtersets, saved jobs
    ├── applications/         # Resume PDF upload, Job Applications, status update pipeline
    ├── notifications/        # Candidate status update notifications & Celery tasks
    └── admin_analytics/      # Admin platform reporting & statistics metrics
```

---

## Quick Start Guide

### 1. Set Up Virtual Environment

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Database Migrations

```bash
python manage.py migrate
```

### 5. Seed Initial Sample Data

Populates sample accounts (Admin, Employer, Candidate), Job Listings, Resume, Applications, and Notifications:
```bash
python manage.py seed_data
```

**Created Default Credentials:**
- **Admin**: Username: `admin`, Password: `Admin@123`
- **Employer**: Username: `techcorp_emp`, Password: `Employer@123`
- **Candidate**: Username: `john_cand`, Password: `Candidate@123`

### 6. Run Development Server

```bash
python manage.py runserver
```

Server will run at `http://127.0.0.1:8000/`.

### 7. Run Celery Worker (Optional)

```bash
celery -A config worker -l info
```

---

## API Documentation (Swagger & Redoc)

Interactive API documentation and schema endpoints are available out of the box:

- **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Redoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- **OpenAPI Schema (JSON)**: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## Summary of API Endpoints

### 🔐 Authentication (`/api/auth/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register new user (`candidate` or `employer`) | Public |
| `POST` | `/api/auth/login/` | User login (returns access & refresh JWT tokens) | Public |
| `POST` | `/api/auth/logout/` | Logout user (blacklists refresh token) | Authenticated |
| `POST` | `/api/auth/refresh-token/` | Refresh JWT access token | Public |
| `POST` | `/api/auth/change-password/` | Change account password | Authenticated |
| `POST` | `/api/auth/verify-email/` | Verify candidate/employer email | Public / Auth |

### 👤 Profiles & Candidate (`/api/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` / `PUT` | `/api/candidate/profile/` | View/Update candidate profile details | Candidate |
| `GET` / `PUT` | `/api/employer/profile/` | View/Update company profile details | Employer |
| `POST` | `/api/resumes/upload/` | Upload resume (PDF only, max 5MB) | Candidate |
| `GET` | `/api/resumes/` | List uploaded resumes | Candidate |
| `DELETE` | `/api/resumes/{id}/` | Delete specific resume | Candidate Owner |

### 💼 Jobs (`/api/jobs/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/jobs/` | List active jobs (with pagination, filters, & sorting) | Public |
| `GET` | `/api/jobs/{id}/` | Retrieve job details | Public |
| `GET` | `/api/jobs/search/` | Search jobs by title, description, skills, location | Public |
| `POST` | `/api/jobs/` | Post new job listing | Employer |
| `PUT`/`PATCH`/`DELETE` | `/api/jobs/{id}/` | Update or delete job posting | Employer Owner |
| `GET` | `/api/employer/jobs/` | List all jobs created by authenticated employer | Employer |
| `GET` / `POST` | `/api/saved-jobs/` | List / Save jobs | Candidate |
| `DELETE` | `/api/saved-jobs/{id}/` | Unsave job | Candidate Owner |

### 📑 Job Applications (`/api/applications/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/applications/` | Track all submitted job applications | Candidate |
| `POST` | `/api/applications/` | Apply for a job (prevents duplicate applications) | Candidate |
| `GET` | `/api/jobs/{id}/applicants/` | View applicants for a posted job | Employer Owner |
| `PATCH` | `/api/applications/{id}/status/` | Update application status & dispatch notification | Employer Owner |

### 🔔 Notifications (`/api/notifications/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/notifications/` | View candidate status update notifications | Authenticated |
| `PATCH` | `/api/notifications/{id}/read/` | Mark notification as read | Authenticated |

### 📊 Admin Analytics (`/api/admin/`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| `GET` | `/api/admin/stats/` | View aggregate platform metrics & statistics | Admin |

---

## Running Test Suite

Run the full automated unit and integration test suite:

```bash
python manage.py test apps.accounts.tests apps.jobs.tests apps.applications.tests apps.notifications.tests apps.admin_analytics.tests
```

15 tests cover registration, JWT tokens, RBAC permissions, resume PDF validation, duplicate application prevention, filtering/search, status updates, and admin metrics.
