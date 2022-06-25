from datetime import datetime
from app import db

class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mata_kuliah = db.Column(db.String(100))
    tanggal =db.Column(db.Date, nullable=False, default=datetime.utcnow)
    start_time = db.Column(db.String(50))
    end_time = db.Column(db.String(50))
    link = db.Column(db.String(100))

    def __init__(self, mata_kuliah, start_time, end_time, link):
        self.mata_kuliah = mata_kuliah
        self.start_time = start_time
        self.end_time = end_time
        self.link = link