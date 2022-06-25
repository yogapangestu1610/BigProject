from app import app
import os
import cv2
import pandas as pd
import numpy as np
import mtcnn
import glob
from werkzeug.utils import secure_filename
from flask import request, jsonify

UPLOAD_FOLDER = 'images/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

facerecognition_model = ("bin/frozen_graph.pb")
labels_filename = ("bin/labels.csv")
facedetection_model = ("bin/haarcascade_frontalface_default.xml")
use_mtcnn=False
load_gambar = (cv2.imread(file) for file in glob.glob("images/*"))

def __init__(self, facerecognition_model = "frozen_graph.pb", 
                    labels_filename="labels.csv", 
                    facedetection_model="haarcascade_frontalface_default.xml",
                    use_mtcnn = False,
                    load_gambar=(cv2.imread(file) for file in glob.glob("images/*"))):
    
    if os.path.isfile(labels_filename) == False:
        raise Exception("Can't find %s" % labels_filename)
        
    self.labels = pd.read_csv(labels_filename)['0'].values
    self.use_mtcnn = use_mtcnn

    self.load_gambar = load_gambar

    if self.use_mtcnn :
        self.face_cascade = MTCNN()
    else :
        self.face_cascade = cv2.CascadeClassifier(facedetection_model)
    
    self.net = cv2.dnn.readNet(facerecognition_model)
    self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    self.layerOutput = self.net.getUnconnectedOutLayersNames()


def predict(self, frame):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = []
    if self.use_mtcnn :
        faces = detector.detect_faces(img)
        faces = [ face['box'] for face in faces]
    else :
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        
    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (50, 50))

        blob = cv2.dnn.blobFromImage(face_img, 1.0, (50, 50), (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(blob)
        output = self.net.forward(self.layerOutput)

        idx = output[0].argmax(axis=1)[0]
        confidence = output[0].max(axis=1)[0]*100

        if confidence > 70:
            curr_label = self.labels[idx]
            faces.append(curr_label)

        else :
            label_text = "N/A"
        frame = self.draw_ped(frame, label_text, x, y, x + w, y + h, color=(0,255,255), text_color=(50,50,50))
    
    print('ini faces '+ faces)
    return faces


def draw_ped(self, img, label, x0, y0, xt, yt, color=(255,127,0), text_color=(255,255,255)):
    (w, h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 1)
    cv2.rectangle(img,
                    (x0, y0 + baseline),  
                    (max(xt, x0 + w), yt), 
                    color, 
                    2)
    cv2.rectangle(img,
                    (x0, y0 - h),  
                    (x0 + w, y0 + baseline), 
                    color, 
                    -1)  
    cv2.putText(img, 
                label, 
                (x0, y0),                   
                cv2.FONT_HERSHEY_SIMPLEX,     
                0.8,                          
                text_color,                
                1,
                cv2.LINE_AA) 
    return img

def gen_frames(self):  
        while True:
            success, frame = self.load_gambar
            if not success:
                break
            else:
                try :
                    frame = self.predict(frame)
                    print('ini frame '+frame)
                except :
                    print("[ERROR] Can't recognize the face.")
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def result():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")

    ruangan = request.form['ruangan']
    kelas = request.form['kelas']
    mata_kuliah = request.form['mata_kuliah']
    id_dosen = request.form['id_dosen']

    if 'image' not in request.files:
        resp = jsonify({'msg': "No body image attached in request"})
        resp.status_code = 501
        return resp
    
    image = request.files['image']

    if image.filename == '':
        resp = jsonify({'msg': "No file image selected"})
        resp.status_code = 404
        return resp
    error = {}
    success = False

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        success = True
    else:
        error[image.filename] = "File type is not allowed"

    if success and error:
        error['Message'] = "File not uploaded"
        resp = jsonify(error)
        resp.status_code = 500
        return resp
    if success:
        try:
            img = load_gambar

            deteksi = predict(img)
            #os.remove(UPLOAD_FOLDER+'/'+filename)

            print('ini deteksi', deteksi)


        except Exception as e:
            resp = {

                'status': 500,
                'msg': "Failed get predict emotion",
                'Error': "Image yang masukan bukan wajah"
            
            }
            error = jsonify(resp)
            error.status_code = 500
            return error
