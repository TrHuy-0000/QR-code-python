import qrcode

def generate_common_qr():
    url = "https://qr-code-python.onrender.com"

    qr = qrcode.make(url)
    qr.save("common_qr.png")
    print("Mã QR chung đã được tạo! Quét để mở trang điểm danh.")

generate_common_qr()
