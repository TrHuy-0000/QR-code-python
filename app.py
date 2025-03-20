from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Danh sách người hợp lệ và trạng thái điểm danh
valid_users = {
    "Nguyen Van A": {"stt": "001", "status": "red"},
    "Tran Thi B": {"stt": "002", "status": "red"}
}

@app.route("/")
def home():
    return render_template("form.html")  # Giao diện nhập thông tin

@app.route("/admin")
def admin():
    return render_template("admin.html", users=valid_users)  # Giao diện quản lý

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    stt = request.form.get("stt")

    if name in valid_users and valid_users[name]["stt"] == stt:
        valid_users[name]["status"] = "green"  # Cập nhật trạng thái
        return jsonify({"status": "success", "message": "Điểm danh thành công!", "color": "green"})
    else:
        return jsonify({"status": "error", "message": "Thông tin không hợp lệ!", "color": "red"})

@app.route("/get_status")
def get_status():
    return jsonify(valid_users)  # Gửi dữ liệu danh sách cập nhật

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
