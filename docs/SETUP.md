# Hướng Dẫn Cài Đặt Hệ Thống - BDU Support

## 1. Yêu Cầu Hệ Thống

### 1.1. Phần Cứng (Recommended)
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4 GB | 8 GB |
| Storage | 20 GB SSD | 50 GB SSD |

### 1.2. Phần Mềm
| Software | Version |
|----------|---------|
| Docker | 20.10+ |
| Docker Compose | 2.0+ |
| Python (nếu không dùng Docker) | 3.8+ |
| MySQL | 8.0 |
| Redis | 6.0+ |

---

## 2. Cài Đặt Với Docker (Khuyến nghị)

### 2.1. Clone Repository

```bash
git clone https://github.com/your-repo/bduSupport.git
cd bduSupport
```

### 2.2. Chuẩn Bị Firebase Certificate

#### Bước 1: Tạo Firebase Project
1. Truy cập [Firebase Console](https://console.firebase.google.com/)
2. Tạo project mới hoặc sử dụng project hiện có
3. Vào **Project Settings > Service Accounts**
4. Click **Generate new private key**
5. Download file JSON

#### Bước 2: Đặt file certificate
```bash
# Development
cp path/to/your/firebase-key.json firebase_cert.dev.json

# Production
cp path/to/your/firebase-key.json firebase_cert.json
```

#### Bước 3: (Optional) Mã hóa file với GPG
```bash
# Mã hóa
gpg --symmetric --cipher-algo AES256 firebase_cert.json

# Giải mã
gpg --decrypt firebase_cert.json.gpg > firebase_cert.json
```

### 2.3. Cấu Hình Environment

#### Development Mode
File `docker-compose.dev.yaml` đã được cấu hình sẵn. Chỉ cần cập nhật các biến sau nếu cần:

```yaml
environment:
  - DATABASE_ENGINE=mysql
  - DATABASE_NAME=bdusupport
  - DATABASE_USER=root
  - DATABASE_PASSWORD=bdusupport
  - DATABASE_HOST=bdusupport_mysql
  - DATABASE_PORT=3306
  - REDIS_HOST=bdusupport_redis
  - REDIS_PORT=6379
  - EMAIL_HOST_USER=your_email@gmail.com
  - EMAIL_HOST_PASSWORD=your_app_password
  - FIREBASE_CERTIFICATE=/usr/src/app/firebase_cert.dev.json
  - FIREBASE_STORAGE_BUCKET_URL=your-project.appspot.com
  - BDU_DATA_WAREHOUSE_GATEWAY_BASE_URL=https://cds.bdu.edu.vn/data
  - BDU_DATA_WAREHOUSE_GATEWAY_USERNAME=
  - BDU_DATA_WAREHOUSE_GATEWAY_PASSWORD=
```

#### Production Mode
Tạo file `.env` hoặc cập nhật `docker-compose.yaml`:

```env
# Database
DATABASE_ENGINE=mysql
DATABASE_NAME=bdusupport
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=your_db_host
DATABASE_PORT=3306

# Redis
REDIS_HOST=your_redis_host
REDIS_PORT=6379
REDIS_USERNAME=default
REDIS_PASSWORD=your_redis_password

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Firebase
FIREBASE_CERTIFICATE=/usr/src/app/firebase_cert.json
FIREBASE_STORAGE_BUCKET_URL=your-project.appspot.com

# BDU Data Warehouse
BDU_DATA_WAREHOUSE_GATEWAY_BASE_URL=https://cds.bdu.edu.vn/data
BDU_DATA_WAREHOUSE_GATEWAY_USERNAME=your_username
BDU_DATA_WAREHOUSE_GATEWAY_PASSWORD=your_password

# Logging
BETTERSTACK_LOG_TOKEN=your_betterstack_token
```

### 2.4. Khởi Chạy Hệ Thống

#### Development
```bash
# Build và khởi chạy
docker-compose -f docker-compose.dev.yaml up --build

# Chạy ở background
docker-compose -f docker-compose.dev.yaml up -d --build

# Xem logs
docker-compose -f docker-compose.dev.yaml logs -f
```

#### Production
```bash
# Build và khởi chạy
docker-compose up --build -d

# Xem logs
docker-compose logs -f
```

### 2.5. Chạy Migrations

```bash
# Development
docker-compose -f docker-compose.dev.yaml exec bdusupport_backend python manage.py migrate

# Production
docker-compose exec bdusupport_backend python manage.py migrate
```

### 2.6. Tạo Superuser

```bash
# Development
docker-compose -f docker-compose.dev.yaml exec bdusupport_backend python manage.py createsuperuser

# Production
docker-compose exec bdusupport_backend python manage.py createsuperuser
```

### 2.7. Kiểm Tra Hệ Thống

```bash
# Health check
curl http://localhost:8000/apis/health

# Swagger UI
open http://localhost:8000/swagger/
```

---

## 3. Cài Đặt Thủ Công (Không Docker)

### 3.1. Cài Đặt Dependencies

#### Ubuntu/Debian
```bash
# Update system
sudo apt-get update

# Install Python
sudo apt-get install python3 python3-pip python3-dev

# Install MySQL client
sudo apt-get install default-libmysqlclient-dev build-essential pkg-config

# Install Redis
sudo apt-get install redis-server
```

#### macOS
```bash
# Install Homebrew (nếu chưa có)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python mysql redis
```

### 3.2. Tạo Virtual Environment

```bash
# Tạo virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
# hoặc
.\venv\Scripts\activate   # Windows

# Install packages
pip install -r requirements.txt
```

### 3.3. Cấu Hình Database

#### Tạo Database MySQL
```sql
CREATE DATABASE bdusupport CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bdusupport'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON bdusupport.* TO 'bdusupport'@'localhost';
FLUSH PRIVILEGES;
```

#### Start Redis
```bash
# Linux
sudo systemctl start redis

# macOS
brew services start redis
```

### 3.4. Cấu Hình Environment Variables

Tạo file `.env` ở thư mục gốc:

```env
DATABASE_ENGINE=mysql
DATABASE_NAME=bdusupport
DATABASE_USER=bdusupport
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USERNAME=default
REDIS_PASSWORD=

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

FIREBASE_CERTIFICATE=firebase_cert.json
FIREBASE_STORAGE_BUCKET_URL=your-project.appspot.com

BDU_DATA_WAREHOUSE_GATEWAY_BASE_URL=https://cds.bdu.edu.vn/data
BDU_DATA_WAREHOUSE_GATEWAY_USERNAME=
BDU_DATA_WAREHOUSE_GATEWAY_PASSWORD=

BETTERSTACK_LOG_TOKEN=your_token
```

### 3.5. Chạy Migrations

```bash
python manage.py migrate
```

### 3.6. Tạo Superuser

```bash
python manage.py createsuperuser
```

### 3.7. Khởi Chạy Server

#### Django Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Với Gunicorn (Production)
```bash
gunicorn BDUSuportBE.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 3.8. Khởi Chạy Celery

#### Celery Worker
```bash
celery -A BDUSuportBE worker -l INFO
```

#### Celery Beat (Scheduler)
```bash
celery -A BDUSuportBE beat -l INFO
```

---

## 4. Cấu Hình Email (Gmail SMTP)

### 4.1. Bật 2-Factor Authentication
1. Truy cập [Google Account](https://myaccount.google.com/)
2. Vào **Security > 2-Step Verification**
3. Bật 2FA

### 4.2. Tạo App Password
1. Sau khi bật 2FA, vào **Security > App passwords**
2. Chọn **Mail** và **Other (Custom name)**
3. Đặt tên: "BDU Support"
4. Copy password được tạo
5. Sử dụng password này cho `EMAIL_HOST_PASSWORD`

---

## 5. Cấu Hình Firebase

### 5.1. Tạo Firebase Project
1. Truy cập [Firebase Console](https://console.firebase.google.com/)
2. Click **Add project**
3. Nhập tên project, follow các bước

### 5.2. Cấu Hình Storage
1. Vào **Build > Storage**
2. Click **Get started**
3. Chọn location và security rules
4. Copy bucket URL (vd: `your-project.appspot.com`)

### 5.3. Cấu Hình Cloud Messaging
1. Vào **Project Settings > Cloud Messaging**
2. Enable Cloud Messaging API
3. (Optional) Cấu hình Web Push certificates

---

## 6. Cấu Hình BDU Data Warehouse

Liên hệ với BDU IT Department để lấy:
- Base URL
- Username
- Password

---

## 7. Nginx Configuration (Production)

### 7.1. Install Nginx
```bash
sudo apt-get install nginx
```

### 7.2. Cấu Hình Virtual Host

Tạo file `/etc/nginx/sites-available/bdusupport`:

```nginx
server {
    listen 80;
    server_name api.bdusupport.edu.vn;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/bduSupport/static/;
    }
}
```

### 7.3. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/bdusupport /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7.4. SSL với Let's Encrypt
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.bdusupport.edu.vn
```

---

## 8. Troubleshooting

### 8.1. Database Connection Error

**Lỗi:** `Can't connect to MySQL server`

**Giải pháp:**
```bash
# Kiểm tra MySQL đang chạy
docker-compose ps
# hoặc
sudo systemctl status mysql

# Kiểm tra connection
mysql -h localhost -u bdusupport -p
```

### 8.2. Redis Connection Error

**Lỗi:** `Error connecting to Redis`

**Giải pháp:**
```bash
# Kiểm tra Redis
docker-compose ps
# hoặc
redis-cli ping
```

### 8.3. Celery Worker Not Processing

**Lỗi:** Tasks không được xử lý

**Giải pháp:**
```bash
# Kiểm tra worker logs
docker-compose logs bdusupport_worker

# Restart worker
docker-compose restart bdusupport_worker
```

### 8.4. Firebase Error

**Lỗi:** `Firebase initialization failed`

**Giải pháp:**
- Kiểm tra path đến certificate file
- Verify certificate content
- Kiểm tra quyền truy cập file

### 8.5. Migration Error

**Lỗi:** `Relation already exists`

**Giải pháp:**
```bash
# Fake migration
python manage.py migrate --fake

# hoặc reset migrations
python manage.py migrate --fake-initial
```

---

## 9. Backup & Restore

### 9.1. Backup Database

```bash
# MySQL dump
docker-compose exec bdusupport_mysql mysqldump -u root -p bdusupport > backup.sql

# hoặc từ host
mysqldump -h localhost -P 3307 -u root -p bdusupport > backup.sql
```

### 9.2. Restore Database

```bash
# Restore
docker-compose exec -T bdusupport_mysql mysql -u root -p bdusupport < backup.sql
```

### 9.3. Backup Redis

```bash
# Redis RDB
docker-compose exec bdusupport_redis redis-cli BGSAVE
```

---

## 10. Monitoring

### 10.1. Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f bdusupport_backend
```

### 10.2. Health Check

```bash
# API health
curl http://localhost:8000/apis/health

# Database
docker-compose exec bdusupport_mysql mysqladmin -u root -p ping

# Redis
docker-compose exec bdusupport_redis redis-cli ping
```

### 10.3. BetterStack/Logtail

Logs được tự động gửi đến BetterStack nếu `BETTERSTACK_LOG_TOKEN` được cấu hình.

---

## 11. Update & Deployment

### 11.1. Pull Latest Code

```bash
git pull origin main
```

### 11.2. Rebuild & Restart

```bash
# Rebuild
docker-compose build

# Restart với zero-downtime
docker-compose up -d --no-deps --build bdusupport_backend

# Run migrations
docker-compose exec bdusupport_backend python manage.py migrate
```

### 11.3. Rollback

```bash
git checkout <previous_commit>
docker-compose up -d --build
```

---

## 12. Docker Commands Reference

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Stop
docker-compose down

# Restart specific service
docker-compose restart bdusupport_backend

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec bdusupport_backend python manage.py shell

# Clean up
docker-compose down -v --rmi all
```

---

## 13. Ports Reference

| Service | Internal Port | External Port |
|---------|---------------|---------------|
| Backend | 8000 | 8000 |
| MySQL | 3306 | 3307 |
| Redis | 6379 | 6380 |

---

## 14. Security Checklist

- [ ] Thay đổi default passwords
- [ ] Cấu hình HTTPS với SSL
- [ ] Giới hạn ALLOWED_HOSTS
- [ ] Tắt DEBUG mode trong production
- [ ] Cấu hình firewall
- [ ] Enable rate limiting
- [ ] Backup định kỳ
- [ ] Monitoring và alerting

---

## 15. Hỗ Trợ

Nếu gặp vấn đề, liên hệ:
- Email: ntthuan060102.work@gmail.com
- Issues: [GitHub Issues](https://github.com/your-repo/bduSupport/issues)

