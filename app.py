import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)

# Định nghĩa Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    integer = db.Column(db.String(50), nullable=False)  # Chuyển Integer -> String
    decimal = db.Column(db.String(50), nullable=False)  # Chuyển Float -> String
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default="red")  # Trạng thái mặc định là chưa điểm danh

# Khởi tạo database nếu chưa có
with app.app_context():
    db.create_all()

# Trang chủ
@app.route("/")
def home():
    return render_template("form.html")

# API: Điểm danh
@app.route('/check_user', methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        if not data or 'integer' not in data or 'decimal' not in data or 'name' not in data:
            return jsonify({"message": "Thiếu dữ liệu!"}), 400

        user = User.query.filter_by(integer=str(data['integer']), decimal=str(data['decimal']), name=data['name'].strip()).first()

        if user:
            user.status = "green"  # Cập nhật trạng thái đã điểm danh
            db.session.commit()
            return jsonify({"message": "Điểm danh thành công!"}), 200
        else:
            return jsonify({"message": "Thông tin không chính xác!"}), 400

    except Exception as e:
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500

# Trang admin
@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

# Thư mục lưu file upload
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# API: Upload file Excel
@app.route("/upload_excel", methods=["POST"])
def upload_excel():
    if "file" not in request.files:
        return jsonify({"message": "Không tìm thấy file"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Chưa chọn file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        df = pd.read_excel(file_path, dtype=str)  # Đọc file Excel
        df['integer'] = df['integer'].astype(str)
        df['decimal'] = df['decimal'].astype(str)
        users = df.to_dict(orient="records")  # Chuyển thành danh sách dict

        # Lưu dữ liệu vào database
        for user in users:
            new_user = User(
                integer=str(user['integer']),
                decimal=str(user['decimal']),
                name=user['name'].strip()
            )
            db.session.add(new_user)

        db.session.commit()  # Lưu vào database

        return jsonify({"message": "Tải lên thành công!", "data": users})
    except Exception as e:
        return jsonify({"message": "Lỗi xử lý file: " + str(e)}), 500

# API: Lấy danh sách users
@app.route("/get_users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_list = [
        {
            "id": user.id,
            "integer": user.integer,
            "decimal": user.decimal,
            "name": user.name,
            "status": user.status,
        }
        for user in users
    ]
    return jsonify(users_list)

# API: Thêm user mới
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        print("Dữ liệu nhân: ", data)
        if not data or 'integer' not in data or 'decimal' not in data or 'name' not in data:
            return jsonify({"message": "Thiếu dữ liệu!"}), 400

        new_user = User(
            integer=str(data['integer']),
            decimal=str(data['decimal']),
            name=data['name'].strip()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Thêm thành công!"}), 201

    except Exception as e:
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500

# API: Xóa user
@app.route("/delete_user", methods=["POST"])
def delete_user():
    data = request.get_json()
    if "id" not in data:
        return jsonify({"status": "error", "message": "Thiếu ID!"}), 400

    user = User.query.filter_by(id=data["id"]).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "Xóa thành công!"})
    
    return jsonify({"status": "error", "message": "Không tìm thấy người dùng!"})

# Trang danh sách điểm danh
@app.route("/grid")
def grid():
    return render_template("grid.html")

# Chạy Flask server
if __name__ == "__main__":
    app.run(debug=True)
