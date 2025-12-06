# Tài Liệu Nghiệp Vụ - BDU Support

## 1. Tổng Quan Hệ Thống

**BDU Support** là hệ thống hỗ trợ tuyển sinh và giám sát sinh viên cho Trường Đại học Bình Dương (Binh Duong University - BDU). Hệ thống được thiết kế để phục vụ các đối tượng sau:

- **Thí sinh/Học sinh**: Đăng ký xét tuyển, tra cứu thông tin ngành học, đặt lịch tư vấn
- **Sinh viên**: Theo dõi thời khóa biểu, điểm số, điểm danh
- **Phụ huynh**: Giám sát tình hình học tập của sinh viên
- **Quản trị viên (Admin)**: Quản lý toàn bộ hệ thống
- **Super Admin (Root)**: Quản lý tài khoản admin và cấu hình hệ thống

## 2. Các Module Nghiệp Vụ Chính

### 2.1. Module Quản Lý Tuyển Sinh (Admission Registration)

#### 2.1.1. Mô tả nghiệp vụ
Cho phép thí sinh đăng ký xét tuyển vào các ngành học của trường thông qua Zalo Mini App.

#### 2.1.2. Quy trình nghiệp vụ

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Thí sinh đăng  │────▶│  Hệ thống nhận   │────▶│  Admin xét     │
│  ký qua MiniApp │     │  hồ sơ (pending) │     │  duyệt hồ sơ   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                        ┌──────────────────┐              │
                        │  Gửi email thông │◀─────────────┘
                        │  báo kết quả     │
                        └──────────────────┘
```

#### 2.1.3. Các phương thức xét tuyển (Evaluation Methods)
- **Điểm thi THPT Quốc gia** (HighSchoolGraduationExam): Xét điểm thi tốt nghiệp THPT
- **Điểm thi đánh giá năng lực** (CompetencyAssessmentExam): Xét điểm thi ĐGNL
- **Học bạ lớp 10, 11, 12** (Grades_10_11_12): Xét điểm học bạ 3 năm THPT
- **Học bạ lớp 12** (Grade_12): Xét điểm học bạ lớp 12
- **5 học kỳ THPT** (FiveSemestersOfHighSchool): Xét điểm 5 học kỳ

#### 2.1.4. Trạng thái hồ sơ
| Trạng thái | Mô tả |
|------------|-------|
| `pending` | Đang chờ xét duyệt |
| `approved` | Đã được duyệt |
| `rejected` | Bị từ chối |

#### 2.1.5. Tiêu chí đánh giá đậu/trượt
- **Điểm thi THPT QG**: `final_score >= benchmark_30`
- **Điểm ĐGNL**: `final_score >= benchmark_competency_assessment_exam`
- **Điểm học bạ**: `final_score >= benchmark_school_record`

---

### 2.2. Module Quản Lý Ngành Học (Major Management)

#### 2.2.1. Mô tả
Quản lý thông tin các ngành học được mở tuyển sinh.

#### 2.2.2. Thông tin ngành học
| Thuộc tính | Mô tả |
|------------|-------|
| Mã ngành (code) | Mã định danh ngành học |
| Tên ngành (name) | Tên đầy đủ của ngành |
| Năm tuyển sinh (year) | Năm áp dụng |
| Chỉ tiêu (expected_target) | Số lượng chỉ tiêu tuyển sinh |
| Học phí (tuition_fee) | Học phí/kỳ |
| Số tín chỉ (number_of_credits) | Tổng số tín chỉ chương trình |
| Điểm chuẩn 30 (benchmark_30) | Điểm chuẩn xét theo THPT QG |
| Điểm chuẩn học bạ (benchmark_school_record) | Điểm chuẩn xét học bạ |
| Điểm chuẩn ĐGNL (benchmark_competency_assessment_exam) | Điểm chuẩn ĐGNL |
| Trạng thái tuyển sinh (open_to_recruitment) | Có đang mở tuyển hay không |

#### 2.2.3. Liên kết
- **Bậc đào tạo (Academic Level)**: Cao đẳng, Đại học, Thạc sĩ,...
- **Cơ sở đào tạo (Training Location)**: Địa điểm học
- **Tổ hợp xét tuyển (College Exam Group)**: A00, A01, D01,...
- **Phương thức xét tuyển (Evaluation Method)**: Các phương thức xét tuyển cho ngành

---

### 2.3. Module Đặt Lịch Tư Vấn (Reservation)

#### 2.3.1. Mô tả
Cho phép thí sinh đặt lịch hẹn tư vấn tuyển sinh với nhà trường.

#### 2.3.2. Thông tin đặt lịch
- Họ tên, ngày sinh, CCCD/CMND
- Trường THPT, lớp, tỉnh/thành phố
- Số điện thoại, Zalo, email
- Địa chỉ
- Ngành quan tâm

---

### 2.4. Module Giám Sát Sinh Viên (Student Supervision)

#### 2.4.1. Mô tả
Cho phép phụ huynh đăng ký theo dõi tình hình học tập của sinh viên.

#### 2.4.2. Quy trình nghiệp vụ

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Phụ huynh đăng │────▶│  Liên kết với    │────▶│  Nhận thông báo │
│  ký giám sát    │     │  mã sinh viên    │     │  định kỳ        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

#### 2.4.3. Thông tin giám sát
- **Điểm danh (Attendance)**: Thông báo khi sinh viên vắng mặt
- **Điểm số (Scores)**: Kết quả học tập theo học kỳ
- **Thời khóa biểu (Timetable)**: Lịch học hàng ngày
- **Xếp loại học lực (Classification)**: Xếp loại học kỳ

#### 2.4.4. Thông báo tự động (Cron Jobs)
- `send_student_attendance_notification`: Gửi thông báo điểm danh hàng ngày
- `send_student_academic_classification_notification`: Gửi thông báo xếp loại học lực

---

### 2.5. Module Tin Tức (News Management)

#### 2.5.1. Mô tả
Quản lý và phát hành tin tức, thông báo từ nhà trường.

#### 2.5.2. Phân loại tin tức
- Tin tức được phân theo **Loại tin (News Type)**
- Mỗi tin có: Tiêu đề, Link bài viết, Hình ảnh, Ngày đăng

---

### 2.6. Module Phản Hồi (Feedback)

#### 2.6.1. Mô tả
Cho phép người dùng MiniApp gửi phản hồi, góp ý đến nhà trường.

#### 2.6.2. Vai trò người phản hồi
- Sinh viên
- Phụ huynh
- Khác

---

### 2.7. Module Liên Hệ (Contact)

#### 2.7.1. Mô tả
Hiển thị và quản lý thông tin liên hệ của các phòng ban trong trường.

---

### 2.8. Module Cẩm Nang (Handbook)

#### 2.8.1. Mô tả
Quản lý các tài liệu hướng dẫn, cẩm nang cho sinh viên/thí sinh.

---

### 2.9. Module Tuyển Dụng Doanh Nghiệp (Business Recruitment)

#### 2.9.1. Mô tả
Đăng tin tuyển dụng từ các doanh nghiệp đối tác cho sinh viên.

#### 2.9.2. Thông tin tin tuyển dụng
- Tên doanh nghiệp
- Vị trí tuyển dụng
- Mô tả công việc
- Link chi tiết
- Banner

---

### 2.10. Module Cơ Sở Vật Chất (Facility)

#### 2.10.1. Mô tả
Giới thiệu hình ảnh, thông tin về cơ sở vật chất của trường.

---

### 2.11. Module Thông Báo (Notification)

#### 2.11.1. Mô tả
Gửi thông báo đẩy (push notification) đến người dùng MiniApp thông qua Firebase Cloud Messaging.

#### 2.11.2. Loại thông báo
- Thông báo hệ thống
- Thông báo điểm danh sinh viên
- Thông báo xếp loại học lực
- Thông báo tuyển sinh

---

## 3. Phân Quyền Hệ Thống

### 3.1. Backoffice (Admin Portal)

| Vai trò | Mô tả | Quyền hạn |
|---------|-------|-----------|
| **Root** | Super Admin | Toàn quyền hệ thống, quản lý Admin |
| **Admin** | Quản trị viên | Quản lý nội dung, xét duyệt hồ sơ |

### 3.2. MiniApp (Zalo Mini App)

| Vai trò | Mô tả |
|---------|-------|
| **Student** | Sinh viên đang theo học |
| **Parent** | Phụ huynh giám sát |
| **Candidate** | Thí sinh tuyển sinh |

---

## 4. Tích Hợp Hệ Thống Bên Ngoài

### 4.1. BDU Data Warehouse
- Lấy thông tin sinh viên
- Lấy điểm danh
- Lấy bảng điểm
- Lấy thời khóa biểu
- Lấy sự kiện sinh viên
- Lấy xếp loại học lực

### 4.2. Zalo API
- Xác thực người dùng MiniApp
- Gửi thông báo Zalo

### 4.3. Firebase
- **Firebase Storage**: Lưu trữ hình ảnh, file
- **Firebase Cloud Messaging (FCM)**: Gửi push notification

### 4.4. Email (SMTP)
- Gửi email thông báo kết quả xét tuyển
- Gửi email OTP xác thực

---

## 5. Quy Trình Nghiệp Vụ Tổng Quan

### 5.1. Quy Trình Tuyển Sinh

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           QUY TRÌNH TUYỂN SINH                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐ │
│  │ Thí sinh│───▶│ Tra cứu     │───▶│ Điền thông  │───▶│ Nộp hồ sơ      │ │
│  │ đăng nhập│   │ ngành học   │    │ tin cá nhân │    │ xét tuyển      │ │
│  └─────────┘    └─────────────┘    └─────────────┘    └─────────────────┘ │
│                                                                │           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │           │
│  │ Nhận email  │◀───│ Xét duyệt   │◀───│ Admin nhận  │◀───────┘           │
│  │ thông báo   │    │ hồ sơ       │    │ hồ sơ       │                    │
│  └─────────────┘    └─────────────┘    └─────────────┘                    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### 5.2. Quy Trình Giám Sát Sinh Viên

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        QUY TRÌNH GIÁM SÁT SINH VIÊN                        │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌───────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │ Phụ huynh │───▶│ Đăng ký     │───▶│ Liên kết    │                      │
│  │ đăng nhập │    │ giám sát    │    │ mã sinh viên│                      │
│  └───────────┘    └─────────────┘    └─────────────┘                      │
│                                              │                             │
│                                              ▼                             │
│  ┌───────────────────────────────────────────────────────────────┐        │
│  │                    THÔNG BÁO TỰ ĐỘNG                          │        │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │        │
│  │  │ Điểm danh    │  │ Điểm số      │  │ Xếp loại học lực │    │        │
│  │  │ hàng ngày    │  │ theo kỳ      │  │ cuối kỳ          │    │        │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘    │        │
│  └───────────────────────────────────────────────────────────────┘        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Thuật Ngữ

| Thuật ngữ | Tiếng Anh | Mô tả |
|-----------|-----------|-------|
| THPT | High School | Trung học phổ thông |
| ĐGNL | Competency Assessment | Đánh giá năng lực |
| Học bạ | School Record | Bảng điểm học sinh |
| Điểm chuẩn | Benchmark | Điểm tối thiểu để đậu |
| Tổ hợp | Exam Group | Nhóm môn xét tuyển (A00, A01,...) |
| Bậc đào tạo | Academic Level | Trình độ đào tạo (CĐ, ĐH, ThS,...) |
| MiniApp | Zalo Mini App | Ứng dụng mini trên Zalo |
| Backoffice | Admin Portal | Trang quản trị hệ thống |

---

## 7. Lịch Sử Phiên Bản

| Version | Ngày | Mô tả |
|---------|------|-------|
| 1.0 | 2024 | Phiên bản khởi tạo |

