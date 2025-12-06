# Tài Liệu Kiến Trúc Hệ Thống - BDU Support

## 1. Tổng Quan Kiến Trúc

### 1.1. Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                         │
├──────────────────────────────────┬──────────────────────────────────────────┤
│         Zalo Mini App            │           Backoffice Web App             │
│    (React/Vue - Zalo SDK)        │         (React/Vue/Angular)              │
└──────────────────────────────────┴──────────────────────────────────────────┘
                    │                                   │
                    │              HTTPS                │
                    ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         NGINX / Load Balancer                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BDU SUPPORT BACKEND                               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    Django REST Framework                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ MiniApp APIs │  │Backoffice API│  │    Swagger/OpenAPI       │  │   │
│  │  │ /apis/miniapp│  │/apis/backoffice  │    /swagger/             │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │                      BUSINESS LOGIC LAYER                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Services   │  │    Tasks     │  │      Middlewares         │  │   │
│  │  │ (BDU DW,OTP) │  │(Celery Tasks)│  │(Auth, Permission, Error) │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────┴───────────────────────────────────┐   │
│  │                         DATA ACCESS LAYER                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ Django ORM   │  │ Serializers  │  │      Validators          │  │   │
│  │  │   Models     │  │              │  │                          │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
          │                    │                        │
          ▼                    ▼                        ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐
│     MySQL       │  │     Redis       │  │     External Services           │
│   (Database)    │  │ (Cache/Broker)  │  │  ┌───────┐ ┌───────┐ ┌───────┐ │
└─────────────────┘  └─────────────────┘  │  │ BDU DW│ │Firebase│ │ Zalo  │ │
                                          │  └───────┘ └───────┘ └───────┘ │
                                          └─────────────────────────────────┘
```

### 1.2. Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Web Framework | Django | 4.2+ |
| REST API | Django REST Framework | Latest |
| API Documentation | drf-yasg (Swagger) | Latest |
| Database | MySQL | 8.0 |
| Cache/Message Broker | Redis | 6.0 |
| Task Queue | Celery | 5.4.0 |
| Task Scheduler | django-celery-beat | 2.7.0 |
| Authentication | djangorestframework-simplejwt | Latest |
| Static Files | Whitenoise | Latest |
| WSGI Server | Gunicorn | Latest |
| Container | Docker | Latest |
| Push Notification | Firebase Admin SDK | Latest |
| File Storage | Firebase Storage | - |
| Logging | Logtail (BetterStack) | Latest |

---

## 2. Cấu Trúc Thư Mục

```
bduSupport/
├── BDUSuportBE/                    # Django Project Settings
│   ├── __init__.py
│   ├── asgi.py                     # ASGI config
│   ├── celery.py                   # Celery config
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Root URL config
│   └── wsgi.py                     # WSGI config
│
├── bduSuport/                      # Main Django App
│   ├── configs/                    # External service configs
│   │   ├── firebase_storage.py
│   │   └── zalo_api.py
│   │
│   ├── const/                      # Constants
│   │   └── provinces.py
│   │
│   ├── errors/                     # Custom exceptions
│   │   └── un_verified_exception.py
│   │
│   ├── helpers/                    # Utility functions
│   │   ├── audit.py                # Audit logging helper
│   │   ├── email.py                # Email helper
│   │   ├── firebase_storage_provider.py
│   │   ├── http.py                 # HTTP utilities
│   │   ├── paginator.py
│   │   └── response.py             # Standard response helper
│   │
│   ├── middlewares/                # Custom middlewares
│   │   ├── backoffice_authentication.py
│   │   ├── custom_exception_handler.py
│   │   ├── custom_user_authentication_rule.py
│   │   ├── miniapp_authentication.py
│   │   └── permissions/            # Permission classes
│   │       ├── is_admin.py
│   │       ├── is_admin_or_root.py
│   │       ├── is_miniapp_user.py
│   │       └── is_root.py
│   │
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── admission_registration.py
│   │   ├── major.py
│   │   ├── mini_app_user.py
│   │   ├── news.py
│   │   └── ... (other models)
│   │
│   ├── serializers/                # DRF Serializers
│   │   ├── account_serializer.py
│   │   ├── major_serializer.py
│   │   └── ... (other serializers)
│   │
│   ├── services/                   # External service integrations
│   │   ├── bdu_dw/                 # BDU Data Warehouse
│   │   │   ├── bdu_dw.py
│   │   │   ├── dto.py
│   │   │   ├── key_mapper.py
│   │   │   └── mapping_dicts.py
│   │   └── otp.py                  # OTP service
│   │
│   ├── tasks/                      # Celery tasks
│   │   ├── bg_tasks.py             # Background tasks
│   │   ├── cron_tasks.py           # Scheduled tasks
│   │   ├── heartbeats.py
│   │   └── biz/
│   │       └── send_student_attendance_notification.py
│   │
│   ├── templates/                  # Email templates
│   │   ├── approve_registration.html
│   │   ├── otp.html
│   │   └── submit_registration.html
│   │
│   ├── validations/                # Request validations
│   │   └── ... (validation files)
│   │
│   ├── views/                      # API Views
│   │   ├── academic_level/
│   │   ├── admission_registration/
│   │   ├── major/
│   │   ├── news/
│   │   ├── notification/
│   │   └── ... (other views)
│   │
│   └── urls.py                     # App URL config
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── BUSINESS.md
│   └── SETUP.md
│
├── docker-compose.yaml             # Production Docker Compose
├── docker-compose.dev.yaml         # Development Docker Compose
├── Dockerfile                      # Main app Dockerfile
├── Dockerfile.beat                 # Celery Beat Dockerfile
├── Dockerfile.worker               # Celery Worker Dockerfile
├── manage.py                       # Django management
└── requirements.txt                # Python dependencies
```

---

## 3. Thành Phần Hệ Thống

### 3.1. Backend Service (Django)

#### Trách nhiệm:
- Xử lý HTTP requests
- Business logic
- Database operations
- API authentication/authorization

#### Cấu hình chính (settings.py):
- Database: MySQL với django ORM
- Cache: Redis với django-redis
- JWT: djangorestframework-simplejwt
- Static files: Whitenoise
- Logging: Logtail (BetterStack)

### 3.2. Celery Worker

#### Trách nhiệm:
- Xử lý background tasks
- Gửi email async
- Gửi push notification
- Các tác vụ nặng

#### Cấu hình:
```python
CELERY_BROKER_URL = REDIS_CONN_STR
CELERY_RESULT_BACKEND = REDIS_CONN_STR
CELERY_TIMEZONE = "Asia/Ho_Chi_Minh"
```

### 3.3. Celery Beat

#### Trách nhiệm:
- Scheduled tasks
- Cron jobs
- Gửi thông báo định kỳ

#### Cấu hình:
- Sử dụng django-celery-beat
- Tasks được định nghĩa trong admin interface hoặc database

### 3.4. MySQL Database

#### Trách nhiệm:
- Persistent data storage
- Relational data management

#### Các bảng chính:
- `account` - Tài khoản backoffice
- `mini_app_user` - Người dùng MiniApp
- `admission_registration` - Hồ sơ tuyển sinh
- `major` - Ngành học
- `news` - Tin tức
- `reservation` - Đặt lịch
- `student_supervision_registration` - Đăng ký giám sát

### 3.5. Redis

#### Trách nhiệm:
- Caching
- Celery message broker
- Session storage (optional)

---

## 4. Authentication & Authorization

### 4.1. Backoffice Authentication

```
┌────────────┐     ┌─────────────────┐     ┌────────────────┐
│   Client   │────▶│   Login API     │────▶│ JWT Token Pair │
│            │     │                 │     │ (access/refresh)│
└────────────┘     └─────────────────┘     └────────────────┘
       │                                            │
       │           ┌─────────────────┐              │
       └──────────▶│  Protected API  │◀─────────────┘
                   │ (Bearer Token)  │
                   └─────────────────┘
```

#### Token Lifetime:
- Access Token: 180 minutes
- Refresh Token: 30 days

### 4.2. MiniApp Authentication

```
┌────────────┐     ┌─────────────────┐     ┌────────────────┐
│ Zalo User  │────▶│   Zalo OAuth    │────▶│  User Info     │
│            │     │                 │     │                │
└────────────┘     └─────────────────┘     └────────────────┘
       │                                            │
       │           ┌─────────────────┐              │
       └──────────▶│ MiniApp Auth API│◀─────────────┘
                   │ (Get/Create User)│
                   └─────────────────┘
```

### 4.3. Permission Classes

| Permission Class | Mô tả |
|-----------------|-------|
| `IsRoot` | Chỉ Super Admin |
| `IsAdmin` | Chỉ Admin |
| `IsAdminOrRoot` | Admin hoặc Super Admin |
| `IsMiniappUser` | Người dùng MiniApp đã xác thực |

---

## 5. Tích Hợp Hệ Thống Bên Ngoài

### 5.1. BDU Data Warehouse

```
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│  BDU Support    │────▶│  BDU DW Gateway     │────▶│  Data Warehouse │
│   Backend       │     │  (REST API)         │     │                 │
└─────────────────┘     └─────────────────────┘     └─────────────────┘
```

#### Endpoints sử dụng:
| Endpoint | Mô tả |
|----------|-------|
| `/fact_ho_so_sinh_vien_odp` | Hồ sơ sinh viên |
| `/dim_danh_sach_diem_danh_odp` | Điểm danh |
| `/dim_bang_diem_odp` | Bảng điểm |
| `/dim_thoi_khoa_bieu_odp` | Thời khóa biểu |
| `/dim_su_kien_odp` | Sự kiện sinh viên |
| `/dim_xep_loai_hoc_ki_odp` | Xếp loại học kỳ |

### 5.2. Firebase

#### Firebase Storage
- Lưu trữ hình ảnh (news, facilities, banners)
- Lưu trữ file đính kèm

#### Firebase Cloud Messaging (FCM)
- Push notification đến MiniApp users
- Thông báo điểm danh, điểm số

### 5.3. Email (SMTP)

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

---

## 6. Data Flow

### 6.1. Đăng Ký Xét Tuyển

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   MiniApp   │────▶│   Backend   │────▶│   MySQL     │────▶│  Admin      │
│   (POST)    │     │ Validation  │     │  (Store)    │     │  Review     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
┌─────────────┐     ┌─────────────┐     ┌─────────────┐            │
│   Student   │◀────│   SMTP      │◀────│  Celery     │◀───────────┘
│   (Email)   │     │  (Gmail)    │     │  (Async)    │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 6.2. Thông Báo Điểm Danh

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Celery Beat │────▶│   Task      │────▶│   BDU DW    │────▶│ Attendance  │
│  (Schedule) │     │ (Worker)    │     │   (API)     │     │   Data      │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Parent    │◀────│    FCM      │◀────│ Notification│
│  (MiniApp)  │     │  (Push)     │     │  (Create)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 7. Database Schema (ERD)

```
┌────────────────────┐     ┌────────────────────┐
│      Account       │     │    MiniAppUser     │
├────────────────────┤     ├────────────────────┤
│ id (PK)            │     │ id (PK)            │
│ email (UNIQUE)     │     │ mini_app_user_id   │
│ phone              │     │ name               │
│ status             │     │ avatar_url         │
│ role (admin/root)  │     └─────────┬──────────┘
│ created_at         │               │
│ updated_at         │               │
└─────────┬──────────┘               │
          │                          │
          │ reviewed_by              │ user
          ▼                          ▼
┌────────────────────────────────────────────────────────┐
│                  AdmissionRegistration                  │
├─────────────────────────────────────────────────────────┤
│ id (PK)                                                 │
│ user (FK -> MiniAppUser)                               │
│ student (FK -> Student)                                │
│ major (FK -> Major)                                    │
│ evaluation_method (FK -> EvaluationMethod)             │
│ college_exam_group (FK -> CollegeExamGroup)            │
│ reviewed_by (FK -> Account)                            │
│ review_status (pending/approved/rejected)              │
│ created_at, recalled_at                                │
└─────────────────────────────────────────────────────────┘
          │
          │ major
          ▼
┌────────────────────────────────────────────────────────┐
│                        Major                            │
├─────────────────────────────────────────────────────────┤
│ id (PK)                                                 │
│ code, name, description                                │
│ year, expected_target                                  │
│ benchmark_30, benchmark_school_record                  │
│ benchmark_competency_assessment_exam                   │
│ tuition_fee, number_of_credits                         │
│ training_location (FK -> TrainingLocation)             │
│ academic_level (FK -> AcademicLevel)                   │
│ open_to_recruitment                                    │
│ created_at, updated_at, deleted_at                     │
└─────────────────────────────────────────────────────────┘
          │
          │ M2M
          ▼
┌─────────────────────┐     ┌─────────────────────┐
│  CollegeExamGroup   │     │  EvaluationMethod   │
├─────────────────────┤     ├─────────────────────┤
│ id, code, name      │     │ id, code, name      │
│ subjects (M2M)      │     │                     │
└─────────────────────┘     └─────────────────────┘
```

---

## 8. Security

### 8.1. Authentication
- JWT-based authentication với HMAC SHA256
- Token rotation khi refresh
- Blacklist tokens sau khi rotation

### 8.2. Authorization
- Role-based access control (RBAC)
- Permission classes cho từng endpoint
- Middleware authentication

### 8.3. Data Protection
- Password hashing với bcrypt
- CORS enabled (configurable origins)
- Input validation với serializers

### 8.4. Logging & Monitoring
- Centralized logging với Logtail/BetterStack
- Exception tracking
- Task monitoring với heartbeats

---

## 9. Deployment Architecture

### 9.1. Docker Compose (Development/Production)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Backend (8000) │  │  Worker         │  │  Beat           │ │
│  │  Django/Gunicorn│  │  Celery Worker  │  │  Celery Beat    │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │          │
│           │        ┌───────────┴───────────┐        │          │
│           └───────▶│       Redis (6379)    │◀───────┘          │
│                    │    Broker/Cache       │                   │
│                    └───────────────────────┘                   │
│                                                                 │
│                    ┌───────────────────────┐                   │
│                    │     MySQL (3306)      │                   │
│                    │      Database         │                   │
│                    └───────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2. Environment Variables

| Variable | Mô tả |
|----------|-------|
| `DATABASE_ENGINE` | mysql/postgresql |
| `DATABASE_NAME` | Tên database |
| `DATABASE_USER` | Database username |
| `DATABASE_PASSWORD` | Database password |
| `DATABASE_HOST` | Database host |
| `DATABASE_PORT` | Database port |
| `REDIS_HOST` | Redis host |
| `REDIS_PORT` | Redis port |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `FIREBASE_CERTIFICATE` | Path to Firebase cert |
| `FIREBASE_STORAGE_BUCKET_URL` | Firebase Storage bucket |
| `BDU_DATA_WAREHOUSE_GATEWAY_*` | BDU DW credentials |
| `BETTERSTACK_LOG_TOKEN` | Logtail token |

---

## 10. Scalability Considerations

### 10.1. Horizontal Scaling
- Stateless backend (JWT-based auth)
- External session storage (Redis)
- Multiple Celery workers

### 10.2. Performance
- Database connection pooling
- Redis caching
- Async task processing
- Pagination (20 items/page default)

### 10.3. High Availability
- Docker container restart policies
- Redis data persistence
- MySQL volume persistence

---

## 11. Monitoring & Logging

### 11.1. Application Logging
```python
LOGGING = {
    "handlers": {
        "logtail": {
            "class": "logtail.LogtailHandler",
            "source_token": BETTERSTACK_LOG_TOKEN
        },
        "console": {
            "class": "logging.StreamHandler"
        }
    }
}
```

### 11.2. Task Monitoring
- Heartbeats gửi đến monitoring service
- Celery task tracking với result backend
- Task timeout: 30 minutes

### 11.3. Health Check
- `/apis/health` endpoint
- Docker health checks

---

## 12. Phiên Bản & Changelog

| Version | Ngày | Thay đổi |
|---------|------|----------|
| 1.0 | 2024 | Initial release |

