from keras.models import load_model
import numpy as np
import pickle
import cv2
import tensorflow as tf
from preprocess_images import preprocess_image
from resize import resize_image
MODEL_FILENAME = "model/captcha_model.txt"
MODEL_LABELS_FILENAME = "model/model_labels.txt"

def load_captcha_model(model_filename = MODEL_FILENAME,labels_filename = MODEL_LABELS_FILENAME):

	model = load_model(model_filename)

	graph = tf.get_default_graph()
	with open(labels_filename,"rb") as f:
		lb = pickle.load(f)
	return (model,graph,lb)
    
def solve_captcha(image_file,model_data):
	#image = cv2.imread(image_file)
	(model,graph,lb) = model_data
	letter_images = preprocess_image(image_file)

	if not letter_images:
		return ""

	#create ảnh output và ds các ký tự dự đoán
	#output = cv2.merge([image]*3)
	predictions=[]

	for letter_image in letter_images:
		letter_image=resize_image(letter_image,20,20)

		letter_image = np.expand_dims(letter_image, axis=2)
		letter_image = np.expand_dims(letter_image,axis = 0)
		with graph.as_default():
			#yêu cầu NR đưa ra dự đoán
			prediction = model.predict(letter_image)
        #chuyển ký tự đc dự đoán thành ký str
		letter = lb.inverse_transform(prediction)[0]
		predictions.append(letter)
      
	captcha_text = "".join(predictions)
	#cv2.imshow("OUT",output)
	#cv2.waitKey()
	return captcha_text

