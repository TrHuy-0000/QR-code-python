from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Danh sách người hợp lệ
valid_users = {
    "Nguyen Van A": "001",
    "Tran Thi B": "002"
}

@app.route("/")
def home():
    return render_template("form.html")  # Gửi trang web chứa form

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    stt = request.form.get("stt")

    if name in valid_users and valid_users[name] == stt:
        return jsonify({"status": "success", "message": "Điểm danh thành công!", "color": "green"})
    else:
        return jsonify({"status": "error", "message": "Thông tin không hợp lệ!", "color": "red"})

if __name__ == "__main__":
    app.run(debug=True)
