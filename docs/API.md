# Tài Liệu API - BDU Support

## 1. Tổng Quan

### 1.1. Base URL
```
Production: https://api.bdusupport.edu.vn/apis
Development: http://localhost:8000/apis
```

### 1.2. API Documentation
Swagger UI có sẵn tại: `/swagger/`

### 1.3. Authentication
API sử dụng JWT (JSON Web Token) cho xác thực.

**Header:**
```
Authorization: Bearer <access_token>
```

### 1.4. Response Format

#### Thành công (2xx)
```json
{
    "status": true,
    "message": "Success message",
    "data": { ... }
}
```

#### Lỗi (4xx, 5xx)
```json
{
    "status": false,
    "message": "Error message",
    "errors": { ... }
}
```

### 1.5. Pagination
```json
{
    "count": 100,
    "next": "http://api.example.com/resource?page=2",
    "previous": null,
    "results": [ ... ]
}
```
- Default page size: 20 items

---

## 2. API Endpoints

### 2.1. Health Check

| Endpoint | Method | Auth | Mô tả |
|----------|--------|------|-------|
| `/apis/health` | GET | No | Kiểm tra trạng thái hệ thống |
| `/apis/media` | GET | No | Lấy media files |

---

## 3. Backoffice APIs (`/apis/backoffice/`)

### 3.1. Authentication

#### 3.1.1. Đăng nhập
```http
POST /apis/backoffice/login
```

**Request Body:**
```json
{
    "email": "admin@bdu.edu.vn",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 3.1.2. Refresh Token
```http
POST /apis/backoffice/refresh
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 3.2. Account Management

#### 3.2.1. Lấy danh sách tài khoản Admin
```http
GET /apis/backoffice/admin/accounts
```
**Auth:** Required (Admin/Root)

#### 3.2.2. Tạo tài khoản Admin
```http
POST /apis/backoffice/admin/accounts
```
**Auth:** Required (Root only)

**Request Body:**
```json
{
    "email": "newadmin@bdu.edu.vn",
    "phone": "0901234567",
    "password": "secure_password"
}
```

#### 3.2.3. Quản lý tài khoản cá nhân
```http
GET /apis/backoffice/accounts
PUT /apis/backoffice/accounts/{id}
```

---

### 3.3. Major Management (Quản lý ngành học)

#### 3.3.1. Lấy danh sách ngành
```http
GET /apis/backoffice/majors
```

**Query Parameters:**
| Param | Type | Mô tả |
|-------|------|-------|
| `year` | int | Lọc theo năm |
| `academic_level` | int | Lọc theo bậc đào tạo |
| `open_to_recruitment` | bool | Lọc theo trạng thái tuyển sinh |
| `page` | int | Số trang |

#### 3.3.2. Tạo ngành mới
```http
POST /apis/backoffice/majors
```

**Request Body:**
```json
{
    "code": "7480201",
    "name": "Công nghệ thông tin",
    "year": 2024,
    "expected_target": 100,
    "benchmark_30": 20.0,
    "benchmark_school_record": 21.0,
    "benchmark_competency_assessment_exam": 600,
    "tuition_fee": 15000000,
    "number_of_credits": 130,
    "description": "Ngành CNTT",
    "training_location": 1,
    "academic_level": 1,
    "college_exam_groups": [1, 2, 3],
    "evaluation_methods": [1, 2, 3]
}
```

#### 3.3.3. Cập nhật ngành
```http
PUT /apis/backoffice/majors/{id}
```

#### 3.3.4. Xóa ngành (Soft delete)
```http
DELETE /apis/backoffice/majors/{id}
```

---

### 3.4. Admission Registration (Quản lý hồ sơ tuyển sinh)

#### 3.4.1. Lấy danh sách hồ sơ
```http
GET /apis/backoffice/admission-registration
```

**Query Parameters:**
| Param | Type | Mô tả |
|-------|------|-------|
| `review_status` | string | pending/approved/rejected |
| `major` | int | Lọc theo ngành |
| `page` | int | Số trang |

#### 3.4.2. Chi tiết hồ sơ
```http
GET /apis/backoffice/admission-registration/{id}
```

#### 3.4.3. Duyệt hồ sơ
```http
PUT /apis/backoffice/admission-registration/{id}
```

**Request Body:**
```json
{
    "review_status": "approved"
}
```

---

### 3.5. News Management (Quản lý tin tức)

#### 3.5.1. CRUD tin tức
```http
GET    /apis/backoffice/news
POST   /apis/backoffice/news
GET    /apis/backoffice/news/{id}
PUT    /apis/backoffice/news/{id}
DELETE /apis/backoffice/news/{id}
```

**Request Body (POST/PUT):**
```json
{
    "title": "Thông báo tuyển sinh 2024",
    "link": "https://bdu.edu.vn/news/1234",
    "image": "https://storage.googleapis.com/...",
    "type": 1,
    "posted_at": "2024-01-15T10:00:00Z"
}
```

#### 3.5.2. News Types
```http
GET    /apis/backoffice/news-types
POST   /apis/backoffice/news-types
PUT    /apis/backoffice/news-types/{id}
DELETE /apis/backoffice/news-types/{id}
```

---

### 3.6. Facility Management (Quản lý cơ sở vật chất)

```http
GET    /apis/backoffice/facilities
POST   /apis/backoffice/facilities
PUT    /apis/backoffice/facilities/{id}
DELETE /apis/backoffice/facilities/{id}
```

```http
GET    /apis/backoffice/facility-images
POST   /apis/backoffice/facility-images
DELETE /apis/backoffice/facility-images/{id}
```

---

### 3.7. Handbook Management (Quản lý cẩm nang)

```http
GET    /apis/backoffice/handbooks
POST   /apis/backoffice/handbooks
PUT    /apis/backoffice/handbooks/{id}
DELETE /apis/backoffice/handbooks/{id}
```

---

### 3.8. Contact Management (Quản lý liên hệ)

```http
GET    /apis/backoffice/contact
POST   /apis/backoffice/contact
PUT    /apis/backoffice/contact/{id}
DELETE /apis/backoffice/contact/{id}
```

---

### 3.9. Feedback Management (Quản lý phản hồi)

```http
GET /apis/backoffice/feedbacks
GET /apis/backoffice/feedbacks/{id}
```

---

### 3.10. Reservation Management (Quản lý đặt lịch)

```http
GET /apis/backoffice/reservations
GET /apis/backoffice/reservations/{id}
```

---

### 3.11. Business Recruitment Management

```http
GET    /apis/backoffice/business-recruiments
POST   /apis/backoffice/business-recruiments
PUT    /apis/backoffice/business-recruiments/{id}
DELETE /apis/backoffice/business-recruiments/{id}
```

---

### 3.12. MiniApp Notification Management

```http
GET    /apis/backoffice/miniapp-notifications
POST   /apis/backoffice/miniapp-notifications
GET    /apis/backoffice/miniapp-notifications/{id}
```

**Request Body (POST):**
```json
{
    "title": "Thông báo quan trọng",
    "content": "Nội dung thông báo",
    "target_users": [1, 2, 3]
}
```

---

### 3.13. Other Management APIs

| Resource | Endpoint |
|----------|----------|
| Academic Levels | `/apis/backoffice/academic-levels` |
| Subjects | `/apis/backoffice/subjects` |
| Evaluation Methods | `/apis/backoffice/evaluation-methods` |
| College Exam Groups | `/apis/backoffice/college-exam-groups` |
| Training Locations | `/apis/backoffice/training-location` |
| App Functions | `/apis/backoffice/app-functions` |
| Audit Logs | `/apis/backoffice/audit` |

---

### 3.14. Super Admin APIs (Root only)

```http
GET    /apis/backoffice/super-admin
POST   /apis/backoffice/super-admin/accounts/backoffice
PUT    /apis/backoffice/super-admin/accounts/backoffice/{id}
DELETE /apis/backoffice/super-admin/accounts/backoffice/{id}
```

---

## 4. MiniApp APIs (`/apis/miniapp/`)

### 4.1. Authentication

#### 4.1.1. Đăng ký/Đăng nhập
```http
POST /apis/miniapp/auth
```

**Request Body:**
```json
{
    "mini_app_user_id": "zalo_user_id_123",
    "name": "Nguyễn Văn A",
    "avatar_url": "https://zalo.vn/avatar/..."
}
```

**Response:**
```json
{
    "status": true,
    "data": {
        "id": 1,
        "mini_app_user_id": "zalo_user_id_123",
        "name": "Nguyễn Văn A",
        "avatar_url": "https://zalo.vn/avatar/..."
    }
}
```

---

### 4.2. Init (Constructor)

```http
GET /apis/miniapp/init
```

Lấy thông tin khởi tạo cho app (config, user info, etc.)

---

### 4.3. News

#### 4.3.1. Lấy danh sách tin tức
```http
GET /apis/miniapp/news
```

**Query Parameters:**
| Param | Type | Mô tả |
|-------|------|-------|
| `type` | int | Lọc theo loại tin |
| `page` | int | Số trang |

#### 4.3.2. Chi tiết tin tức
```http
GET /apis/miniapp/news/{id}
```

---

### 4.4. Majors

#### 4.4.1. Lấy danh sách ngành
```http
GET /apis/miniapp/majors
```

**Query Parameters:**
| Param | Type | Mô tả |
|-------|------|-------|
| `year` | int | Năm tuyển sinh |
| `academic_level` | int | Bậc đào tạo |
| `search` | string | Tìm kiếm theo tên/mã |

#### 4.4.2. Chi tiết ngành
```http
GET /apis/miniapp/majors/{id}
```

---

### 4.5. Admission Registration

#### 4.5.1. Lấy danh sách đăng ký của user
```http
GET /apis/miniapp/admission-registration
```
**Auth:** Required (MiniApp User)

#### 4.5.2. Tạo đăng ký mới
```http
POST /apis/miniapp/admission-registration
```
**Auth:** Required (MiniApp User)

**Request Body:**
```json
{
    "major": 1,
    "evaluation_method": 1,
    "college_exam_group": 1,
    "student": {
        "fullname": "Nguyễn Văn A",
        "gender": true,
        "date_of_birth": "2006-01-15",
        "citizen_id": "012345678901",
        "email": "nguyenvana@gmail.com",
        "phone": "0901234567",
        "address": "123 Đường ABC",
        "city": "Bình Dương",
        "high_school": "THPT Dĩ An"
    },
    "subject_scores": [
        {"subject": 1, "score": 8.5, "grade": 12},
        {"subject": 2, "score": 7.0, "grade": 12},
        {"subject": 3, "score": 8.0, "grade": 12}
    ]
}
```

#### 4.5.3. Chi tiết đăng ký
```http
GET /apis/miniapp/admission-registration/{id}
```

#### 4.5.4. Rút hồ sơ
```http
DELETE /apis/miniapp/admission-registration/{id}
```

---

### 4.6. Reservation (Đặt lịch tư vấn)

#### 4.6.1. Lấy danh sách đặt lịch
```http
GET /apis/miniapp/reservation
```

#### 4.6.2. Tạo đặt lịch
```http
POST /apis/miniapp/reservation
```

**Request Body:**
```json
{
    "major": 1,
    "full_name": "Nguyễn Văn A",
    "birthday": "2006-01-15T00:00:00Z",
    "school_name": "THPT Dĩ An",
    "class_name": "12A1",
    "province": "binh_duong",
    "phone_number": "0901234567",
    "zalo_phone_number": "0901234567",
    "citizen_id_card": "012345678901",
    "email": "nguyenvana@gmail.com",
    "address": "123 Đường ABC, Dĩ An"
}
```

---

### 4.7. Student Supervision (Giám sát sinh viên)

#### 4.7.1. Đăng ký giám sát
```http
POST /apis/miniapp/student-supervision-registration
```

**Request Body:**
```json
{
    "student_dw_code": 12345678,
    "student_full_name": "Nguyễn Văn B"
}
```

#### 4.7.2. Lấy danh sách đăng ký
```http
GET /apis/miniapp/student-supervision-registration
```

#### 4.7.3. Hủy đăng ký
```http
DELETE /apis/miniapp/student-supervision-registration/{id}
```

#### 4.7.4. Lấy thông tin sinh viên
```http
GET /apis/miniapp/student-supervision
```

**Query Parameters:**
| Param | Type | Mô tả |
|-------|------|-------|
| `student_code` | string | Mã sinh viên |
| `type` | string | attendance/scores/timetable/events/classification |
| `date` | date | Ngày (cho attendance/timetable) |
| `semester` | int | Học kỳ (cho scores) |
| `academic_year` | int | Năm học (cho scores) |

---

### 4.8. Feedback

```http
POST /apis/miniapp/feedbacks
```

**Request Body:**
```json
{
    "title": "Góp ý về dịch vụ",
    "content": "Nội dung góp ý chi tiết...",
    "feedbacker_role": "student",
    "phone_number": "0901234567"
}
```

---

### 4.9. Contacts

```http
GET /apis/miniapp/contacts
```

---

### 4.10. Handbooks

```http
GET /apis/miniapp/handbooks
```

---

### 4.11. Business Recruitments

```http
GET /apis/miniapp/business-recruiments
GET /apis/miniapp/business-recruiments/{id}
```

---

### 4.12. Academic Levels

```http
GET /apis/miniapp/academic-levels
```

---

### 4.13. Training Locations

```http
GET /apis/miniapp/training-location
```

---

### 4.14. Facilities

```http
GET /apis/miniapp/facilities
GET /apis/miniapp/facilities/{id}
```

---

### 4.15. Notifications

```http
GET /apis/miniapp/miniapp-notification
GET /apis/miniapp/miniapp-notification/{id}
```

---

### 4.16. Personal App Functions

```http
GET  /apis/miniapp/personal-app-func
POST /apis/miniapp/personal-app-func
```

---

### 4.17. Config

```http
GET /apis/miniapp/config
```

Lấy cấu hình app (version, feature flags, etc.)

---

## 5. Anonymous APIs (`/apis/backoffice/anonymous/`)

### 5.1. Account Recovery

```http
POST /apis/backoffice/anonymous/account/forgot-password
POST /apis/backoffice/anonymous/account/reset-password
```

---

## 6. Error Codes

| HTTP Status | Mô tả |
|-------------|-------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing/Invalid token |
| 403 | Forbidden - No permission |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

---

## 7. Rate Limiting

Hiện tại chưa có rate limiting. Tuy nhiên nên cân nhắc implement trong production.

---

## 8. Versioning

API hiện tại là version 1. Versioning sẽ được thêm khi cần thiết thông qua URL path (`/v1/`, `/v2/`).

---

## 9. Swagger/OpenAPI

Truy cập Swagger UI để xem documentation chi tiết và test API:

```
http://localhost:8000/swagger/
```

Schema hỗ trợ cả HTTP và HTTPS.

---

## 10. SDK/Client Libraries

Hiện chưa có official SDK. Sử dụng các HTTP client tiêu chuẩn:

- **JavaScript:** Axios, Fetch API
- **Python:** requests, httpx
- **Mobile:** Retrofit (Android), Alamofire (iOS)

---

## 11. Changelog

| Version | Ngày | Thay đổi |
|---------|------|----------|
| 1.0 | 2024 | Initial API documentation |

