from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Danh sách người hợp lệ (tạm lưu trong RAM)
valid_users = {
    "Nguyen Van A": "001",
    "Tran Thi B": "002"
}

@app.route("/")
def home():
    return render_template("form.html")  # Trang điểm danh

@app.route("/admin")
def admin():
    return render_template("admin.html", users=valid_users)  # Trang quản lý

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    stt = data.get("stt")

    if name and stt:
        valid_users[name] = stt
        return jsonify({"status": "success", "message": "Thêm người dùng thành công!", "users": valid_users})
    else:
        return jsonify({"status": "error", "message": "Thiếu thông tin!"})

@app.route("/remove_user", methods=["POST"])
def remove_user():
    data = request.get_json()
    name = data.get("name")

    if name in valid_users:
        del valid_users[name]
        return jsonify({"status": "success", "message": "Xóa người dùng thành công!", "users": valid_users})
    else:
        return jsonify({"status": "error", "message": "Không tìm thấy người dùng!"})

if __name__ == "__main__":
    app.run(debug=True)
