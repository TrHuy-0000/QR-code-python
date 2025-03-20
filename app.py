from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Danh sách người dùng + trạng thái điểm danh
users = {
    
}

@app.route("/")
def home():
    return render_template("form.html")  # Trang điểm danh

@app.route("/admin")
def admin():
    return render_template("admin.html", users=users)  # Trang quản lý

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    stt = request.form.get("stt")

    if name in users and users[name]["stt"] == stt:
        users[name]["status"] = "green"  # Cập nhật trạng thái
        return jsonify({"status": "success", "message": "Điểm danh thành công!", "color": "green"})
    else:
        return jsonify({"status": "error", "message": "Thông tin không hợp lệ!", "color": "red"})

@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    stt = data.get("stt")

    if name and stt:
        users[name] = {"stt": stt, "status": "red"}  # Mặc định trạng thái đỏ
        return jsonify({"status": "success", "message": "Thêm người dùng thành công!", "users": users})
    else:
        return jsonify({"status": "error", "message": "Thiếu thông tin!"})

@app.route("/remove_user", methods=["POST"])
def remove_user():
    data = request.get_json()
    name = data.get("name")

    if name in users:
        del users[name]
        return jsonify({"status": "success", "message": "Xóa người dùng thành công!", "users": users})
    else:
        return jsonify({"status": "error", "message": "Không tìm thấy người dùng!"})

if __name__ == "__main__":
    app.run(debug=True)
