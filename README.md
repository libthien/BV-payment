# BV-Payment - Hệ Thống Phê Duyệt Thanh Toán

Hệ thống quản lý và phê duyệt thanh toán cho bệnh viện, được xây dựng bằng Flask.

## Tính năng

- **Quản lý yêu cầu thanh toán**: Tạo, theo dõi và xử lý yêu cầu thanh toán
- **Quy trình phê duyệt nhiều cấp**: HOD -> Finance -> CFO -> Accounting
- **Dashboard chiến lược**: Theo dõi KPI và xu hướng tài chính
- **Quản lý theo khoa/phòng**: Phân bổ và theo dõi ngân sách theo từng khoa
- **Báo cáo**: Thống kê và xuất báo cáo tài chính

## Vai trò người dùng

| Vai trò | Mô tả |
|---------|-------|
| USER | Nhân viên - Tạo yêu cầu thanh toán |
| HOD | Trưởng khoa - Phê duyệt cấp 1 |
| FINANCE | Tài chính - Phê duyệt cấp 2 |
| CFO | Giám đốc tài chính - Phê duyệt cấp 3 |
| ACCOUNTING | Kế toán - Phê duyệt cuối cùng |
| ADMIN | Quản trị hệ thống |

## Cài đặt

### Yêu cầu

- Python 3.9+
- pip

### Các bước cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd BV-payment
```

2. Tạo virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```bash
python app.py
```

5. Truy cập: http://localhost:5000

## Tài khoản Demo

| Email | Mật khẩu | Vai trò |
|-------|----------|---------|
| user1@vbq.com | 123456 | USER |
| hod@vbq.com | 123456 | HOD |
| finance@vbq.com | 123456 | FINANCE |
| cfo@vbq.com | 123456 | CFO |
| accounting@vbq.com | 123456 | ACCOUNTING |
| admin@vbq.com | 123456 | ADMIN |

## Cấu trúc dự án

```
BV-payment/
├── app.py              # Main application
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── approval_list.html
│   ├── approval_detail.html
│   ├── create_request.html
│   ├── my_requests.html
│   ├── request_detail.html
│   ├── reports.html
│   └── error.html
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## Quy trình phê duyệt

```
USER tạo yêu cầu
       ↓
   PENDING_HOD (Chờ HOD duyệt)
       ↓
 PENDING_FINANCE (Chờ Finance duyệt)
       ↓
   PENDING_CFO (Chờ CFO duyệt)
       ↓
PENDING_ACCOUNTING (Chờ Accounting duyệt)
       ↓
    APPROVED (Đã duyệt)
```

## API Endpoints

- `GET /` - Trang chủ
- `GET /login` - Đăng nhập
- `GET /logout` - Đăng xuất
- `GET /dashboard` - Dashboard
- `GET /requests/create` - Tạo yêu cầu mới
- `GET /requests/my` - Yêu cầu của tôi
- `GET /requests/<id>` - Chi tiết yêu cầu
- `GET /approval` - Danh sách phê duyệt
- `GET /approval/<id>` - Chi tiết phê duyệt
- `GET /reports` - Báo cáo
- `GET /api/stats` - API thống kê

## Phát triển

### Chạy mode development
```bash
FLASK_ENV=development python app.py
```

### Chạy với debug
```bash
python app.py  # Debug mode enabled by default
```

## License

MIT License
