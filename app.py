import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Xóa database cũ nếu có để tạo lại từ đầu
# db_path = "attendance.db"
# if os.path.exists(db_path):
 #    os.remove(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    integer = db.Column(db.String(50), nullable=False)  # Chuyển từ Integer -> String
    decimal = db.Column(db.String(50), nullable=False)  # Chuyển từ Float -> String
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), default="red")  # Trạng thái mặc định là chưa điểm danh

# with app.app_context():
   #  db.create_all()  # Tạo lại database với kiểu dữ liệu mới

@app.route("/")
def home():
    return render_template("form.html")

@app.route('/check_user', methods=['POST'])
def check_user():
    try:
        data = request.get_json()
        if not data or 'integer' not in data or 'decimal' not in data or 'name' not in data:
            return jsonify({"message": "Thiếu dữ liệu!"}), 400

        user = User.query.filter_by(integer=str(data['integer']), decimal=str(data['decimal']), name=data['name'].strip()).first()

        if user:
            user.status = "green"  # Cập nhật trạng thái thành đã điểm danh
            db.session.commit()
            return jsonify({"message": "Điểm danh thành công!"}), 200
        else:
            return jsonify({"message": "Thông tin không chính xác!"}), 400

    except Exception as e:
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

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

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data or 'integer' not in data or 'decimal' not in data or 'name' not in data:
            return jsonify({"message": "Thiếu dữ liệu!"}), 400

        new_user = User(
            integer=str(data['integer']),  # Chuyển thành string
            decimal=str(data['decimal']),  # Chuyển thành string
            name=data['name'].strip()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Thêm thành công!"}), 201

    except Exception as e:
        return jsonify({"message": f"Lỗi server: {str(e)}"}), 500

@app.route("/delete_user", methods=["POST"])
def delete_user():
    data = request.get_json()
    user = User.query.filter_by(id=data["id"]).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"status": "success", "message": "Xóa thành công!"})
    return jsonify({"status": "error", "message": "Không tìm thấy người dùng!"})

@app.route("/grid")
def grid():
    return render_template("grid.html")

if __name__ == "__main__":
    app.run(debug=True)
