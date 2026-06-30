# Sử dụng Image Python chính thức, bản slim để tối ưu hóa dung lượng
FROM python:3.11-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Sao chép file cấu hình thư viện vào trước để tận dụng cơ chế cache layer
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# EXPOSE cổng 8080 ra ngoài mạng nội bộ của container
EXPOSE 8080

# =========================================================================
# CẤU HÌNH BẢO MẬT NON-ROOT (Bắt buộc cho OpenShift Developer Sandbox)
# =========================================================================
# Tạo một user thường có tên là 'secops' với UID là 1001
RUN useradd -u 1001 secops && \
    chown -R 1001:0 /app && \
    chmod -R g=u /app

# Ép hệ thống chuyển sang chạy bằng User vừa tạo, từ bỏ hoàn toàn quyền root
USER 1001

# Lệnh khởi chạy ứng dụng Web
CMD ["python", "app.py"]