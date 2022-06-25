from flask.templating import render_template
from app import app
from flask import request, redirect, session
from app.controllers import authController, jadwalController, predikController

@app.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    return render_template('beranda.html')

@app.route('/masuk', methods=['GET'])
def masuk():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route('/signup', methods=['POST'])
def signUp():
    if request.method == 'GET':
        print("melihat semua user")
    elif request.method == 'POST':
        return authController.signUp()

@app.route('/signin', methods=['POST'])
def signIn():
    return authController.signIn()

@app.route('/buat_jadwal', methods = ['GET', 'POST'])
def createJadwal():
    if not session.get("name"):
        return redirect("/masuk")
    if request.method == 'POST':
        return jadwalController.createJadwal()
    else:
        return render_template('buatJadwal.html')

@app.route("/jadwal")
def jadwal():
    if not session.get("name"):
        return redirect("/masuk")
    return render_template("jadwal.html")

@app.route('/updateJadwal/<id>', methods=['PUT'])
def jadwalDetail(id):
    if not session.get("name"):
        return redirect("/masuk")
    return jadwalController.updateJadwal(id)

@app.route('/deleteJadwal/<int:id>', methods=['DELETE'])
def deleteJadwal(id):
    if not session.get("name"):
        return redirect("/masuk")
    return jadwalController.deleteJadwal(id)

# @app.route('/createJadwal', methods = ['POST'])
# def create():
#     if not session.get("name"):
#         return redirect("/masuk")
#     return jadwalController.createJadwal()

@app.route('/kehadiran')
def kehadiran():
    if not session.get("name"):
        return redirect("/masuk")
    return render_template('kehadiran.html')


@app.route('/predict', methods=['POST'])
def predict():
    return predikController.predict()
