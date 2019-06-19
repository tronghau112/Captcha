
from flask import Flask,render_template,request
import cv2
import requests
import numpy as np
import os
from sklearn.neighbors import KDTree
from flask import request
from io import BytesIO
import base64
from solve_captcha import load_captcha_model, solve_captcha

app = Flask(__name__)

MODEL_FILENAME = "model/captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model/model_labels.dat"
UPLOAD_FOLDER = os.path.basename('predict')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def init():
    global model
    model = load_captcha_model(MODEL_FILENAME, MODEL_LABELS_FILENAME)
@app.route("/")
def start_page():
    print("Start")
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_file():
	file = request.files['image']
	image=cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
	filename = 'TestWeb/'+file.filename

	cv2.imwrite(filename,image)

	path='TestWeb/' + file.filename

	captcha_text = solve_captcha(path, model)
	if captcha_text == '':
		return
	return render_template('index.html',string_result = captcha_text,init=True)
if __name__ == "__main__":
    init()
    app.run(threaded=True, host="0.0.0.0")


