import qrcode

def generate_common_qr():
    url = "http://127.0.0.1:5000"
    qr = qrcode.make(url)
    qr.save("common_qr.png")
    print("Mã QR chung đã được tạo! Quét để mở trang điểm danh.")

generate_common_qr()
