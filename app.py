"""
VBQ PAYMENT - HỆ THỐNG PHÊ DUYỆT THANH TOÁN
Flask Application
"""

import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'vbq-payment-secret-key-2024'

DEMO_MODE = True

departments = [
    "Khoa Nội tổng hợp",
    "Khoa Ngoại tổng hợp",
    "Khoa Sản phụ khoa",
    "Khoa Nhi",
    "Khoa Cấp cứu",
    "Khoa Xét nghiệm",
    "Khoa Chẩn đoán hình ảnh",
    "Khoa Dược",
    "Khoa Hồi sức",
    "Khoa Vật lý trị liệu"
]

demo_users = {
    "user1@vbq.com": {"id": "user1", "email": "user1@vbq.com", "name": "Nguyễn Văn A", "role": "USER", "department": "Khoa Nội tổng hợp", "password": "123456"},
    "user2@vbq.com": {"id": "user2", "email": "user2@vbq.com", "name": "Trần Thị B", "role": "USER", "department": "Khoa Ngoại tổng hợp", "password": "123456"},
    "user3@vbq.com": {"id": "user3", "email": "user3@vbq.com", "name": "Lê Văn C", "role": "USER", "department": "Khoa Sản phụ khoa", "password": "123456"},
    "user4@vbq.com": {"id": "user4", "email": "user4@vbq.com", "name": "Phạm Thị D", "role": "USER", "department": "Khoa Nhi", "password": "123456"},
    "user5@vbq.com": {"id": "user5", "email": "user5@vbq.com", "name": "Nguyễn Văn E", "role": "USER", "department": "Khoa Cấp cứu", "password": "123456"},
    "user6@vbq.com": {"id": "user6", "email": "user6@vbq.com", "name": "Trần Văn F", "role": "USER", "department": "Khoa Xét nghiệm", "password": "123456"},
    "user7@vbq.com": {"id": "user7", "email": "user7@vbq.com", "name": "Lê Thị G", "role": "USER", "department": "Khoa Chẩn đoán hình ảnh", "password": "123456"},
    "user8@vbq.com": {"id": "user8", "email": "user8@vbq.com", "name": "Vũ Văn H", "role": "USER", "department": "Khoa Dược", "password": "123456"},
    "user9@vbq.com": {"id": "user9", "email": "user9@vbq.com", "name": "Nguyễn Thị I", "role": "USER", "department": "Khoa Hồi sức", "password": "123456"},
    "user10@vbq.com": {"id": "user10", "email": "user10@vbq.com", "name": "Trần Văn K", "role": "USER", "department": "Khoa Vật lý trị liệu", "password": "123456"},
    "hod1@vbq.com": {"id": "hod1", "email": "hod1@vbq.com", "name": "Phạm Văn D", "role": "HOD", "department": "Khoa Nội tổng hợp", "password": "123456"},
    "hod2@vbq.com": {"id": "hod2", "email": "hod2@vbq.com", "name": "Hoàng Thị E", "role": "HOD", "department": "Khoa Ngoại tổng hợp", "password": "123456"},
    "hod3@vbq.com": {"id": "hod3", "email": "hod3@vbq.com", "name": "Nguyễn Văn F", "role": "HOD", "department": "Khoa Sản phụ khoa", "password": "123456"},
    "hod4@vbq.com": {"id": "hod4", "email": "hod4@vbq.com", "name": "Trần Thị G", "role": "HOD", "department": "Khoa Nhi", "password": "123456"},
    "hod5@vbq.com": {"id": "hod5", "email": "hod5@vbq.com", "name": "Lê Văn H", "role": "HOD", "department": "Khoa Cấp cứu", "password": "123456"},
    "hod6@vbq.com": {"id": "hod6", "email": "hod6@vbq.com", "name": "Phạm Văn I", "role": "HOD", "department": "Khoa Xét nghiệm", "password": "123456"},
    "hod7@vbq.com": {"id": "hod7", "email": "hod7@vbq.com", "name": "Vũ Thị K", "role": "HOD", "department": "Khoa Chẩn đoán hình ảnh", "password": "123456"},
    "hod8@vbq.com": {"id": "hod8", "email": "hod8@vbq.com", "name": "Nguyễn Văn L", "role": "HOD", "department": "Khoa Dược", "password": "123456"},
    "hod9@vbq.com": {"id": "hod9", "email": "hod9@vbq.com", "name": "Trần Văn M", "role": "HOD", "department": "Khoa Hồi sức", "password": "123456"},
    "hod10@vbq.com": {"id": "hod10", "email": "hod10@vbq.com", "name": "Lê Văn N", "role": "HOD", "department": "Khoa Vật lý trị liệu", "password": "123456"},
    "finance@vbq.com": {"id": "fin1", "email": "finance@vbq.com", "name": "Nguyễn Thị P", "role": "FINANCE", "department": "Tài chính - Kế toán", "password": "123456"},
    "cfo@vbq.com": {"id": "cfo1", "email": "cfo@vbq.com", "name": "Trần Văn Q", "role": "CFO", "department": "Tài chính - Kế toán", "password": "123456"},
    "accounting@vbq.com": {"id": "acc1", "email": "accounting@vbq.com", "name": "Lê Thị R", "role": "ACCOUNTING", "department": "Tài chính - Kế toán", "password": "123456"},
    "admin@vbq.com": {"id": "admin1", "email": "admin@vbq.com", "name": "Admin System", "role": "ADMIN", "department": "Hành chính", "password": "123456"},
}

demo_suppliers = [
    {"id": "sup1", "name": "Công ty TNHH ABC", "tax_code": "0123456789", "address": "123 Đường ABC, TP.HCM"},
    {"id": "sup2", "name": "Công ty CP XYZ", "tax_code": "9876543210", "address": "456 Đường XYZ, Hà Nội"},
    {"id": "sup3", "name": "Nhà cung cấp DEF", "tax_code": "1122334455", "address": "789 Đường DEF, Đà Nẵng"},
    {"id": "sup4", "name": "Công ty TNHH MTV", "tax_code": "5566778899", "address": "321 Đường MNP, Cần Thơ"},
    {"id": "sup5", "name": "Doanh nghiệp tư nhân", "tax_code": "9988776655", "address": "654 Đường QRS, Hải Phòng"},
]

demo_budgets = {
    "Khoa Nội tổng hợp": {"budget": 800000000, "used": 350000000},
    "Khoa Ngoại tổng hợp": {"budget": 900000000, "used": 420000000},
    "Khoa Sản phụ khoa": {"budget": 600000000, "used": 280000000},
    "Khoa Nhi": {"budget": 500000000, "used": 200000000},
    "Khoa Cấp cứu": {"budget": 700000000, "used": 380000000},
    "Khoa Xét nghiệm": {"budget": 400000000, "used": 150000000},
    "Khoa Chẩn đoán hình ảnh": {"budget": 550000000, "used": 220000000},
    "Khoa Dược": {"budget": 450000000, "used": 180000000},
    "Khoa Hồi sức": {"budget": 600000000, "used": 250000000},
    "Khoa Vật lý trị liệu": {"budget": 350000000, "used": 120000000},
    "Tài chính - Kế toán": {"budget": 300000000, "used": 100000000},
}

demo_requests = [
    {
        'id': 'REQ-2026-0001',
        'created_by': 'user1@vbq.com',
        'creator_name': 'Nguyễn Văn A',
        'department': 'Khoa Nội tổng hợp',
        'supplier_id': 'sup1',
        'supplier_name': 'Công ty TNHH ABC',
        'amount': 15000000,
        'content': 'Mua vật tư y tế cho khoa nội',
        'invoice_number': 'HD001/2026',
        'invoice_date': '2026-03-01',
        'status': 'PENDING_HOD',
        'created_at': '2026-03-15 09:30:00',
        'approval_history': []
    },
    {
        'id': 'REQ-2026-0002',
        'created_by': 'user2@vbq.com',
        'creator_name': 'Trần Thị B',
        'department': 'Khoa Ngoại tổng hợp',
        'supplier_id': 'sup2',
        'supplier_name': 'Công ty CP XYZ',
        'amount': 25000000,
        'content': 'Mua dụng cụ phẫu thuật mới',
        'invoice_number': 'HD002/2026',
        'invoice_date': '2026-03-05',
        'status': 'PENDING_HOD',
        'created_at': '2026-03-16 10:15:00',
        'approval_history': []
    },
    {
        'id': 'REQ-2026-0003',
        'created_by': 'user3@vbq.com',
        'creator_name': 'Lê Văn C',
        'department': 'Khoa Sản phụ khoa',
        'supplier_id': 'sup3',
        'supplier_name': 'Nhà cung cấp DEF',
        'amount': 8000000,
        'content': 'Mua thuốc cho khoa sản',
        'invoice_number': 'HD003/2026',
        'invoice_date': '2026-03-10',
        'status': 'PENDING_FINANCE',
        'created_at': '2026-03-12 14:20:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Trưởng khoa Sản', 'action': 'approve', 'note': 'Đã kiểm tra, duyệt', 'timestamp': '2026-03-13 08:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0004',
        'created_by': 'user1@vbq.com',
        'creator_name': 'Nguyễn Văn A',
        'department': 'Khoa Nội tổng hợp',
        'supplier_id': 'sup4',
        'supplier_name': 'Công ty TNHH MTV',
        'amount': 35000000,
        'content': 'Mua máy theo dõi bệnh nhân',
        'invoice_number': 'HD004/2026',
        'invoice_date': '2026-03-08',
        'status': 'PENDING_FINANCE',
        'created_at': '2026-03-11 11:30:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Phạm Văn D', 'action': 'approve', 'note': 'Cần thiết cho công tác điều trị', 'timestamp': '2026-03-12 09:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0005',
        'created_by': 'user2@vbq.com',
        'creator_name': 'Trần Thị B',
        'department': 'Khoa Ngoại tổng hợp',
        'supplier_id': 'sup5',
        'supplier_name': 'Doanh nghiệp tư nhân',
        'amount': 45000000,
        'content': 'Mua thiết bị gây mê',
        'invoice_number': 'HD005/2026',
        'invoice_date': '2026-03-14',
        'status': 'PENDING_CFO',
        'created_at': '2026-03-10 08:45:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Trưởng khoa Ngoại', 'action': 'approve', 'note': 'Cần thiết cho phẫu thuật', 'timestamp': '2026-03-11 10:00:00'},
            {'role': 'FINANCE', 'role_name': 'Nguyễn Thị E', 'action': 'approve', 'note': 'Đã kiểm tra ngân sách', 'timestamp': '2026-03-12 15:30:00'}
        ]
    },
    {
        'id': 'REQ-2026-0006',
        'created_by': 'user3@vbq.com',
        'creator_name': 'Lê Văn C',
        'department': 'Khoa Sản phụ khoa',
        'supplier_id': 'sup1',
        'supplier_name': 'Công ty TNHH ABC',
        'amount': 12000000,
        'content': 'Mua máy siêu âm doppler',
        'invoice_number': 'HD006/2026',
        'invoice_date': '2026-03-16',
        'status': 'PENDING_CFO',
        'created_at': '2026-03-14 13:00:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Trưởng khoa Sản', 'action': 'approve', 'note': 'Phục vụ chẩn đoán thai', 'timestamp': '2026-03-15 09:00:00'},
            {'role': 'FINANCE', 'role_name': 'Nguyễn Thị E', 'action': 'approve', 'note': 'Trong ngân sách khoa', 'timestamp': '2026-03-16 11:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0007',
        'created_by': 'user1@vbq.com',
        'creator_name': 'Nguyễn Văn A',
        'department': 'Khoa Nội tổng hợp',
        'supplier_id': 'sup2',
        'supplier_name': 'Công ty CP XYZ',
        'amount': 20000000,
        'content': 'Mua thuốc điều trị ung thư',
        'invoice_number': 'HD007/2026',
        'invoice_date': '2026-03-15',
        'status': 'PENDING_ACCOUNTING',
        'created_at': '2026-03-08 16:00:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Phạm Văn D', 'action': 'approve', 'note': 'Cần thiết cho điều trị', 'timestamp': '2026-03-09 08:00:00'},
            {'role': 'FINANCE', 'role_name': 'Nguyễn Thị E', 'action': 'approve', 'note': 'Đã verify', 'timestamp': '2026-03-10 10:00:00'},
            {'role': 'CFO', 'role_name': 'Trần Văn F', 'action': 'approve', 'note': 'Approved', 'timestamp': '2026-03-11 14:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0008',
        'created_by': 'user2@vbq.com',
        'creator_name': 'Trần Thị B',
        'department': 'Khoa Ngoại tổng hợp',
        'supplier_id': 'sup3',
        'supplier_name': 'Nhà cung cấp DEF',
        'amount': 18000000,
        'content': 'Mua vật tư phẫu thuật nội soi',
        'invoice_number': 'HD008/2026',
        'invoice_date': '2026-03-17',
        'status': 'PENDING_ACCOUNTING',
        'created_at': '2026-03-13 09:30:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Trưởng khoa Ngoại', 'action': 'approve', 'note': 'Cần cho phẫu thuật', 'timestamp': '2026-03-14 08:00:00'},
            {'role': 'FINANCE', 'role_name': 'Nguyễn Thị E', 'action': 'approve', 'note': 'OK', 'timestamp': '2026-03-15 10:00:00'},
            {'role': 'CFO', 'role_name': 'Trần Văn F', 'action': 'approve', 'note': 'Đồng ý', 'timestamp': '2026-03-16 16:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0009',
        'created_by': 'user3@vbq.com',
        'creator_name': 'Lê Văn C',
        'department': 'Khoa Sản phụ khoa',
        'supplier_id': 'sup4',
        'supplier_name': 'Công ty TNHH MTV',
        'amount': 75000000,
        'content': 'Mua máy monitoring sản khoa',
        'invoice_number': 'HD009/2026',
        'invoice_date': '2026-03-18',
        'status': 'APPROVED',
        'created_at': '2026-03-05 11:00:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Trưởng khoa Sản', 'action': 'approve', 'note': 'Cần thiết cho theo dõi thai', 'timestamp': '2026-03-06 09:00:00'},
            {'role': 'FINANCE', 'role_name': 'Nguyễn Thị E', 'action': 'approve', 'note': 'Trong ngân sách', 'timestamp': '2026-03-07 11:00:00'},
            {'role': 'CFO', 'role_name': 'Trần Văn F', 'action': 'approve', 'note': 'Approved', 'timestamp': '2026-03-08 14:00:00'},
            {'role': 'ACCOUNTING', 'role_name': 'Lê Thị G', 'action': 'approve', 'note': 'Đã thanh toán', 'timestamp': '2026-03-09 10:00:00'}
        ]
    },
    {
        'id': 'REQ-2026-0010',
        'created_by': 'user1@vbq.com',
        'creator_name': 'Nguyễn Văn A',
        'department': 'Khoa Nội tổng hợp',
        'supplier_id': 'sup5',
        'supplier_name': 'Doanh nghiệp tư nhân',
        'amount': 5000000,
        'content': 'Mua đồ dùng văn phòng',
        'invoice_number': 'HD010/2026',
        'invoice_date': '2026-03-19',
        'status': 'REJECTED',
        'created_at': '2026-03-17 15:00:00',
        'approval_history': [
            {'role': 'HOD', 'role_name': 'Phạm Văn D', 'action': 'reject', 'note': 'Đã có đủ vật tư, không cần mua thêm', 'timestamp': '2026-03-18 09:00:00'}
        ]
    }
]
request_counter = 11

APPROVAL_STAGES = ["PENDING_HOD", "PENDING_FINANCE", "PENDING_CFO", "PENDING_ACCOUNTING", "APPROVED", "REJECTED", "INFO_REQUESTED"]

def generate_request_id():
    global request_counter
    year = datetime.now().year
    req_id = f"REQ-{year}-{str(request_counter).zfill(4)}"
    request_counter += 1
    return req_id

def format_currency(amount):
    return f"{amount:,.0f} VNĐ".replace(",", ".")

def get_status_label(status):
    labels = {
        "PENDING_HOD": "Chờ HOD duyệt",
        "PENDING_FINANCE": "Chờ Finance duyệt",
        "PENDING_CFO": "Chờ CFO duyệt",
        "PENDING_ACCOUNTING": "Chờ Accounting duyệt",
        "APPROVED": "Đã duyệt",
        "REJECTED": "Từ chối",
        "INFO_REQUESTED": "Yêu cầu thêm thông tin"
    }
    return labels.get(status, status)

def get_status_class(status):
    classes = {
        "PENDING_HOD": "warning",
        "PENDING_FINANCE": "warning",
        "PENDING_CFO": "warning",
        "PENDING_ACCOUNTING": "warning",
        "APPROVED": "success",
        "REJECTED": "danger",
        "INFO_REQUESTED": "info"
    }
    return classes.get(status, "secondary")

def get_next_stage(current_stage):
    stages = ["PENDING_HOD", "PENDING_FINANCE", "PENDING_CFO", "PENDING_ACCOUNTING", "APPROVED"]
    try:
        idx = stages.index(current_stage)
        if idx < len(stages) - 1:
            return stages[idx + 1]
    except:
        pass
    return current_stage

def check_budget_available(department, amount):
    dept_budget = demo_budgets.get(department, {})
    budget = dept_budget.get('budget', 0)
    used = dept_budget.get('used', 0)
    remaining = budget - used
    return remaining >= amount, remaining, budget, used

def process_auto_approval(request_obj):
    department = request_obj['department']
    amount = request_obj['amount']
    
    is_within_budget, remaining, total_budget, used = check_budget_available(department, amount)
    
    current_status = request_obj['status']
    auto_approved_stages = []
    
    # Define which roles can auto-approve which stages
    stage_to_role = {
        'PENDING_FINANCE': 'FINANCE',
        'PENDING_CFO': 'CFO'
    }
    
    if current_status in stage_to_role and is_within_budget:
        role = stage_to_role[current_status]
        # Check if we already have an auto-approval entry for this role and status to avoid duplicates
        existing_auto = any(
            h.get('role') == role and h.get('action') == 'auto_approve' and h.get('is_auto') is True
            for h in request_obj.get('approval_history', [])
        )
        if not existing_auto:
            request_obj['approval_history'].append({
                'role': role,
                'role_name': 'Hệ thống (Auto)',
                'action': 'auto_approve',
                'note': f'Tự động duyệt - Trong ngân sách (còn {format_currency(remaining)})',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'is_auto': True
            })
            request_obj['status'] = get_next_stage(current_status)
            auto_approved_stages.append(role)
    
    return auto_approved_stages, is_within_budget, remaining, total_budget, used

def can_user_approve(user_role, request_status):
    if user_role == "ADMIN":
        return True
    role_stage_map = {
        "HOD": "PENDING_HOD",
        "FINANCE": "PENDING_FINANCE",
        "CFO": "PENDING_CFO",
        "ACCOUNTING": "PENDING_ACCOUNTING"
    }
    required_stage = role_stage_map.get(user_role)
    return request_status == required_stage

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if session['user']['role'] not in roles and session['user']['role'] != 'ADMIN':
                flash('Bạn không có quyền truy cập trang này!', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if email in demo_users:
            user = demo_users[email]
            if user['password'] == password:
                session['user'] = user
                flash(f'Chào mừng {user["name"]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Mật khẩu không đúng!'
        else:
            error = 'Tài khoản không tồn tại!'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = session['user']
    
    # Basic stats
    total_requests = len(demo_requests)
    pending_requests = len([r for r in demo_requests if r['status'] not in ['APPROVED', 'REJECTED']])
    approved_requests = len([r for r in demo_requests if r['status'] == 'APPROVED'])
    rejected_requests = len([r for r in demo_requests if r['status'] == 'REJECTED'])
    total_amount = sum(r['amount'] for r in demo_requests)
    
    # KPI Data
    total_disbursed = sum(r['amount'] for r in demo_requests if r['status'] == 'APPROVED')
    total_budget = sum(demo_budgets.get(dept, {}).get('budget', 0) for dept in demo_budgets)
    disbursement_rate = round((total_disbursed / total_budget * 100), 1) if total_budget > 0 else 0
    rejection_rate = round((rejected_requests / total_requests * 100), 1) if total_requests > 0 else 0
    
    # Calculate average approval time (mock calculation based on approval history)
    total_approval_time = 0
    count_with_history = 0
    for r in demo_requests:
        if r['approval_history']:
            count_with_history += 1
            # Estimate: each approval takes ~4 hours
            total_approval_time += len(r['approval_history']) * 4
    avg_approval_time = round(total_approval_time / count_with_history, 1) if count_with_history > 0 else 0
    
    kpi_data = {
        'total_disbursed': total_disbursed,
        'total_disbursed_display': format_currency(total_disbursed),
        'disbursement_rate': disbursement_rate,
        'rejection_rate': rejection_rate,
        'avg_approval_time': avg_approval_time
    }
    
    # Monthly trend data (mock)
    monthly_data = [
        {'month': 'T1', 'amount': 150000000},
        {'month': 'T2', 'amount': 180000000},
        {'month': 'T3', 'amount': total_disbursed}
    ]
    
    # Department budget data
    dept_budget_data = {}
    for dept, budget_info in demo_budgets.items():
        dept_budget_data[dept] = {
            'budget': budget_info['budget'],
            'budget_display': format_currency(budget_info['budget']),
            'used': budget_info['used'],
            'used_display': format_currency(budget_info['used'])
        }
    
    # Supplier data
    supplier_amounts = {}
    for r in demo_requests:
        if r['status'] == 'APPROVED':
            supplier_amounts[r['supplier_name']] = supplier_amounts.get(r['supplier_name'], 0) + r['amount']
    supplier_data = sorted([{'name': k, 'amount': v} for k, v in supplier_amounts.items()], 
                          key=lambda x: x['amount'], reverse=True)[:5]
    
    return render_template('dashboard.html', 
                         user=user,
                         total_requests=total_requests,
                         pending_requests=pending_requests,
                         approved_requests=approved_requests,
                         rejected_requests=rejected_requests,
                         total_amount=total_amount,
                         total_amount_display=format_currency(total_amount),
                         kpi_data=kpi_data,
                         monthly_data=monthly_data,
                         dept_budget_data=dept_budget_data,
                         supplier_data=supplier_data)

@app.route('/requests/create', methods=['GET', 'POST'])
@login_required
def create_request():
    user = session['user']
    
    # Get budget info for display in form
    is_within_budget_check, remaining_budget, total_budget, used_budget = check_budget_available(user['department'], 0)
    
    if request.method == 'POST':
        supplier_id = request.form.get('supplier')
        amount = float(request.form.get('amount', 0))
        content = request.form.get('content', '')
        invoice_number = request.form.get('invoice_number', '')
        invoice_date = request.form.get('invoice_date', '')
        
        supplier = next((s for s in demo_suppliers if s['id'] == supplier_id), None)
        
        # Check if request exceeds department budget
        is_within_budget, remaining, total_budget, used = check_budget_available(user['department'], amount)
        
        if not is_within_budget:
            flash(f'Yêu cầu vượt quá ngân sách phòng ban! Ngân sách còn còn: {format_currency(remaining_budget)}. Vui lòng giảm số tiền yêu cầu.', 'error')
            return render_template('create_request.html', user=user, suppliers=demo_suppliers, remaining_budget=remaining_budget)
        
        new_request = {
            'id': generate_request_id(),
            'created_by': user['email'],
            'creator_name': user['name'],
            'department': user['department'],
            'supplier_id': supplier_id,
            'supplier_name': supplier['name'] if supplier else '',
            'amount': amount,
            'content': content,
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'status': 'PENDING_HOD',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'approval_history': []
        }
        
        demo_requests.append(new_request)
        flash('Yêu cầu thanh toán đã được tạo thành công!', 'success')
        return redirect(url_for('my_requests'))
    
    return render_template('create_request.html', user=user, suppliers=demo_suppliers, remaining_budget=remaining_budget)

@app.route('/requests/my')
@login_required
def my_requests():
    user = session['user']
    user_requests = [r for r in demo_requests if r['created_by'] == user['email']]
    user_requests = sorted(user_requests, key=lambda x: x.get('created_at', ''), reverse=True)
    return render_template('my_requests.html', user=user, requests=user_requests, format_currency=format_currency, get_status_label=get_status_label, get_status_class=get_status_class)

@app.route('/requests/<req_id>')
@login_required
def request_detail(req_id):
    user = session['user']
    request_obj = next((r for r in demo_requests if r['id'] == req_id), None)
    
    if not request_obj:
        flash('Yêu cầu không tồn tại!', 'error')
        return redirect(url_for('my_requests'))
    
    # Users can only view requests from their own department
    if user['role'] in ['USER', 'HOD'] and request_obj['department'] != user['department']:
        flash('Bạn không có quyền xem yêu cầu này!', 'error')
        return redirect(url_for('my_requests'))
    
    budget_info = check_budget_available(request_obj['department'], request_obj['amount'])
    
    return render_template('request_detail.html', user=user, request_obj=request_obj, format_currency=format_currency, get_status_label=get_status_label, get_status_class=get_status_class, budget_info=budget_info)

@app.route('/approval')
@login_required
@role_required(['HOD', 'FINANCE', 'CFO', 'ACCOUNTING', 'ADMIN'])
def approval_list():
    user = session['user']
    
    if user['role'] == 'ADMIN':
        pending = [r for r in demo_requests if r['status'] not in ['APPROVED', 'REJECTED']]
    else:
        role_stage_map = {
            'HOD': 'PENDING_HOD',
            'FINANCE': 'PENDING_FINANCE',
            'CFO': 'PENDING_CFO',
            'ACCOUNTING': 'PENDING_ACCOUNTING'
        }
        required_stage = role_stage_map.get(user['role'])
        
        if user['role'] == 'HOD':
            pending = [r for r in demo_requests if r['status'] == required_stage and r['department'] == user['department']]
        else:
            pending = [r for r in demo_requests if r['status'] == required_stage]
        
        # Process auto-approval for Finance and CFO roles
        if user['role'] in ['FINANCE', 'CFO']:
            for request_obj in pending:
                process_auto_approval(request_obj)
    
    pending = sorted(pending, key=lambda x: x.get('created_at', ''), reverse=True)
    return render_template('approval_list.html', user=user, requests=pending, format_currency=format_currency, get_status_label=get_status_label, get_status_class=get_status_class)

@app.route('/approval/<req_id>', methods=['GET', 'POST'])
@login_required
@role_required(['HOD', 'FINANCE', 'CFO', 'ACCOUNTING', 'ADMIN'])
def approval_detail(req_id):
    user = session['user']
    request_obj = next((r for r in demo_requests if r['id'] == req_id), None)
    
    if not request_obj:
        flash('Yêu cầu không tồn tại!', 'error')
        return redirect(url_for('approval_list'))
    
    # HOD can only view requests from their own department
    if user['role'] == 'HOD' and request_obj['department'] != user['department']:
        flash('Bạn không có quyền phê duyệt yêu cầu này!', 'error')
        return redirect(url_for('approval_list'))
    
    if not can_user_approve(user['role'], request_obj['status']):
        flash('Bạn không có quyền phê duyệt yêu cầu này!', 'error')
        return redirect(url_for('approval_list'))
    
    budget_info = check_budget_available(request_obj['department'], request_obj['amount'])
    
    if request.method == 'POST':
        action = request.form.get('action')
        note = request.form.get('note', '')
        
        if not note:
            flash('Vui lòng nhập ghi chú!', 'error')
            return render_template('approval_detail.html', user=user, request_obj=request_obj, format_currency=format_currency, get_status_label=get_status_label, get_status_class=get_status_class, budget_info=budget_info)
        
        if action == 'approve':
            next_stage = get_next_stage(request_obj['status'])
            
            # Always proceed to next stage for HOD approval (special requests go to finance for review)
            request_obj['status'] = next_stage
            
            if next_stage == 'PENDING_FINANCE':
                # Update budget when moving to FINANCE stage (HOD approval)
                # For special requests (exceeding budget), set used to budget (making remaining 0)
                # For normal requests, add the amount as usual
                if request_obj.get('is_special_request', False):
                    # Special request: set used to budget amount (remaining becomes 0)
                    demo_budgets[request_obj['department']]['used'] = demo_budgets[request_obj['department']]['budget']
                else:
                    # Normal request: add the amount to used
                    demo_budgets[request_obj['department']]['used'] += request_obj['amount']
            
            # Add approval record
            approval_record = {
                'role': user['role'],
                'role_name': user['name'],
                'action': action,
                'note': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            request_obj['approval_history'].append(approval_record)
            
            # Process auto-approval for Finance and CFO stages
            auto_stages, is_within_budget, remaining, total_budget, used = process_auto_approval(request_obj)
            
            if auto_stages:
                stage_names = ' và '.join(auto_stages)
                flash(f'Phê duyệt thành công! {stage_names} đã được tự động duyệt do còn trong ngân sách.', 'success')
            else:
                flash('Phê duyệt thành công!', 'success')
        elif action == 'reject':
            request_obj['status'] = 'REJECTED'
            
            # Add approval record
            approval_record = {
                'role': user['role'],
                'role_name': user['name'],
                'action': action,
                'note': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            request_obj['approval_history'].append(approval_record)
            
            flash('Đã từ chối yêu cầu!', 'success')
        elif action == 'request_info':
            request_obj['status'] = 'INFO_REQUESTED'
            
            # Add approval record
            approval_record = {
                'role': user['role'],
                'role_name': user['name'],
                'action': action,
                'note': note,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            request_obj['approval_history'].append(approval_record)
            
            flash('Đã gửi yêu cầu bổ sung thông tin!', 'success')
        
        return redirect(url_for('approval_list'))
    
    return render_template('approval_detail.html', user=user, request_obj=request_obj, format_currency=format_currency, get_status_label=get_status_label, get_status_class=get_status_class, budget_info=budget_info)

@app.route('/reports')
@login_required
@role_required(['ADMIN', 'FINANCE', 'CFO'])
def reports():
    user = session['user']
    
    total_approved = sum(r['amount'] for r in demo_requests if r['status'] == 'APPROVED')
    total_requests = len(demo_requests)
    avg_amount = total_approved / total_requests if total_requests > 0 else 0
    
    status_counts = {}
    for r in demo_requests:
        status_counts[r['status']] = status_counts.get(r['status'], 0) + 1
    
    dept_amounts = {}
    for r in demo_requests:
        dept = r.get('department', 'Unknown')
        dept_amounts[dept] = dept_amounts.get(dept, 0) + r['amount']
    
    return render_template('reports.html',
                         user=user,
                         total_approved=total_approved,
                         total_requests=total_requests,
                         avg_amount=avg_amount,
                         status_counts=status_counts,
                         dept_amounts=dept_amounts,
                         format_currency=format_currency,
                         get_status_label=get_status_label)

@app.route('/approval/history')
@login_required
@role_required(['HOD', 'FINANCE', 'CFO', 'ACCOUNTING', 'ADMIN'])
def approval_history():
    user = session['user']
    
    if user['role'] == 'ADMIN':
        all_approved = [r for r in demo_requests if r['status'] in ['APPROVED', 'REJECTED', 'PENDING_FINANCE', 'PENDING_CFO', 'PENDING_ACCOUNTING']]
    elif user['role'] == 'HOD':
        approved_by_hod = [r for r in demo_requests if r['department'] == user['department'] and any(h['role'] == 'HOD' and h['action'] == 'approve' for h in r.get('approval_history', []))]
        pending_hod = [r for r in demo_requests if r['department'] == user['department'] and r['status'] == 'PENDING_HOD']
        all_approved = approved_by_hod + pending_hod
    elif user['role'] == 'FINANCE':
        approved_by_finance = [r for r in demo_requests if any(h['role'] == 'FINANCE' and h['action'] in ['approve', 'auto_approve'] for h in r.get('approval_history', []))]
        pending_finance = [r for r in demo_requests if r['status'] == 'PENDING_FINANCE']
        all_approved = approved_by_finance + pending_finance
    elif user['role'] == 'CFO':
        approved_by_cfo = [r for r in demo_requests if any(h['role'] == 'CFO' and h['action'] in ['approve', 'auto_approve'] for h in r.get('approval_history', []))]
        pending_cfo = [r for r in demo_requests if r['status'] == 'PENDING_CFO']
        all_approved = approved_by_cfo + pending_cfo
    elif user['role'] == 'ACCOUNTING':
        approved_by_acc = [r for r in demo_requests if any(h['role'] == 'ACCOUNTING' and h['action'] == 'approve' for h in r.get('approval_history', []))]
        pending_acc = [r for r in demo_requests if r['status'] == 'PENDING_ACCOUNTING']
        all_approved = approved_by_acc + pending_acc
    else:
        all_approved = []
    
    all_approved = sorted(all_approved, key=lambda x: x.get('created_at', ''), reverse=True)
    
    return render_template('approval_history.html', 
                         user=user, 
                         requests=all_approved, 
                         format_currency=format_currency, 
                         get_status_label=get_status_label, 
                         get_status_class=get_status_class)

@app.route('/api/stats')
@login_required
def api_stats():
    special_requests = len([r for r in demo_requests if r.get('is_special_request', False)])
    return jsonify({
        'total': len(demo_requests),
        'pending': len([r for r in demo_requests if r['status'] not in ['APPROVED', 'REJECTED']]),
        'approved': len([r for r in demo_requests if r['status'] == 'APPROVED']),
        'rejected': len([r for r in demo_requests if r['status'] == 'REJECTED']),
        'special': special_requests,
        'total_amount': sum(r['amount'] for r in demo_requests)
    })

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error='404 - Trang không tìm thấy'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error='500 - Lỗi server'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)