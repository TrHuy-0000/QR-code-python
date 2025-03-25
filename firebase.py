import firebase_admin
from firebase_admin import credentials, firestore

# Load file JSON (thay thế đường dẫn bằng file của bạn)
cred = credentials.Certificate("D:\Huy\Code\Visual Studio Code\Python\PhamTruongHuy_2001230300\QR python")
firebase_admin.initialize_app(cred)

# Kết nối với Firestore
db = firestore.client()
