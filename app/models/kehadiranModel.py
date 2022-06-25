from sqlalchemy import func
from app import db

class Kehadiran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    mata_kuliah = db.Column(db.String(100))
    waktu = db.Column(db.DateTime(timezone=True), server_default=func.now())
    kehadiran = db.Column(db.String(50))

    def __init__(self, nama, mata_kuliah, kehadiran):
        self.nama = nama
        self.mata_kuliah = mata_kuliah
        self.kehadiran = kehadiran