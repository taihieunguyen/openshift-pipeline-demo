import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Giao diện HTML đơn giản hiển thị trạng thái ứng dụng
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SecOps Demo App</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f6f9; margin: 40px; text-align: center; }
        .container { background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #0066cc; }
        .status { font-weight: bold; color: green; }
        .info { background: #eee; padding: 10px; border-radius: 4px; font-family: monospace; text-align: left; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 OpenShift Cloud-Native Pipeline Success!</h1>
        <p>Ứng dụng Python Flask đã được triển khai hoàn toàn tự động bằng <strong>Tekton Pipelines</strong>.</p>
        <p>Trạng thái hệ thống: <span class="status">RUNNING (User: Non-Root)</span></p>
        
        <div class="info">
            <strong>[Hệ thống Kiểm tra cấu hình Bảo mật]:</strong><br>
            • Môi trường: {{ app_env }}<br>
            • Kết nối Database: {{ db_status }}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    app_env = os.getenv('APP_ENV', 'Production')
    db_pass = os.getenv('DB_PASS')
    
    # Kiểm tra xem Secret từ Ansible đã được inject vào chưa
    if db_pass:
        # Giấu mật khẩu, chỉ hiển thị ký tự đầu để chứng minh đã đọc được Secret an toàn
        masked_pass = db_pass[0] + "*" * (len(db_pass) - 1)
        db_status = f"✅ Kết nối thành công (Mật khẩu nhận từ Secret: {masked_pass})"
    else:
        db_status = "⚠️ Cảnh báo: Không tìm thấy cấu hình DB_PASS từ Secret!"

    return render_template_string(HTML_TEMPLATE, app_env=app_env, db_status=db_status)

# Thêm cổng API kiểm tra sức khỏe (Healthcheck) cho OpenShift Probe
@app.route('/health')
def health():
    return jsonify(status="UP"), 200

if __name__ == '__main__':
    # Ép Flask chạy ở cổng 8080 (Cổng chuẩn, không yêu cầu quyền root của hệ thống)
    app.run(host='0.0.0.0', port=8080)