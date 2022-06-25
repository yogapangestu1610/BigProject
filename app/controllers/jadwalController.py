from app import app
from flask import request, jsonify, render_template, session, redirect
from flask_marshmallow import Marshmallow
from app.models.jadwalModel import db, Jadwal

ma = Marshmallow(app)


class JadwalSchema(ma.Schema):
    class Meta:
        fields = ('id', 'mata_kuliah', 'tanggal', 'start_time', 'end_time')


# init schema
jadwalSchema = JadwalSchema()
jadwalsSchema = JadwalSchema(many=True)



def createJadwal():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    mata_kuliah = request.form['mata_kuliah']
    start_time = request.form['mulai']
    end_time = request.form['selesai'] 
    link = request.form['link']   

    newsJadwal = Jadwal(mata_kuliah=mata_kuliah, start_time=start_time, end_time=end_time, link=link)

    db.session.add(newsJadwal)
    db.session.commit()
    allJadwal = Jadwal.query.all()
    return render_template('jadwal.html', data=enumerate(allJadwal, 1))
    #jsonify({"msg": "success create jadwal", "status": 200, "data": new})


def getAllJadwal():
    if not session.get("name"):
        return redirect("/masuk")
    allJadwal = Jadwal.query.all()
    return render_template('jadwal.html', data=enumerate(allJadwal, 1))

def updateJadwal(id):
    jadwal = Jadwal.query.get(id)
    start_time = request.form['mulai']
    end_time = request.form['selesai'] 
    link = request.form['link']

    jadwal.start_time = start_time
    jadwal.end_time = end_time
    jadwal.link = link

    db.session.commit()
    jadwalUpdate = jadwalSchema.dump(jadwal)
    return jsonify({"msg": "Success update dosen", "status": 200, "data": jadwalUpdate})


def deleteJadwal(id):
    try:
        jadwal = Jadwal.query.filter_by(id=id).first()
        db.session.delete(jadwal)
        db.session.commit()
    except Exception as e:
        print("Failed delete jadwal")
        print(e)
    return redirect('/jadwal')