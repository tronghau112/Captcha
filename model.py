import cv2
import pickle
import os.path
import numpy as np
from imutils import paths
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense
from resize import resize_image

OUTPUT_FOLDER = "output_char"
MODEL_FILENAME = "model/captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model/model_labels.dat"

data = []
labels = []

for image_file in paths.list_images(OUTPUT_FOLDER):
	#load hinh anh va convert qua grayscale

	image = cv2.imread(image_file)
	image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#resize letter sang 20x20 pixel

	image = resize_image(image,20,20)

	#add thong so thu 3 cho Keras

	image = np.expand_dims(image,axis = 2)
	# lấy tên chữ cái dựa vào thư mục

	label = image_file.split(os.path.sep)[-2]
	#add ký tự vào nhãn vào data train

	data.append(image)
	labels.append(label)

data=np.array(data,dtype = "float")/255.0
labels = np.array(labels)

#chia data train thành các bộ train và test riêng

(X_train,X_test,Y_train,Y_test) = train_test_split(data,labels,test_size = 0.25 , random_state = 0)

#convert labels

lb = LabelBinarizer().fit(Y_train)
Y_train=lb.transform(Y_train)
Y_test=lb.transform(Y_test)

#lưu vào model
with open(MODEL_LABELS_FILENAME,"wb") as f:
	pickle.dump(lb,f)

#build neural network

model = Sequential()

#convolutional layer đầu tiên vs max pooling(tổng hợp)

model.add(Conv2D(20,(5,5),padding = "same",input_shape = (20,20,1),activation = "relu")) #relu có tác dụng đưa gia trị âm thành 0
model.add(MaxPooling2D(pool_size = (2,2),strides = (2,2)))
#Stride được hiểu là khoảng cách dịch chuyển của bộ lọc sau mỗi lần tính

#convolutional layer thứ 2 vs max pooling(tổng hợp)

model.add(Conv2D(50,(5,5),padding = "same",activation = "relu"))
model.add(MaxPooling2D(pool_size = (2,2),strides = (2,2)))


#ẩn layer vs 500 nodes

model.add(Flatten())
model.add(Dense(500,activation="relu"))

#output vs 36 nodes mỗi node ứng vs 1 chữ cái hoặc 1 số dự đoán
#Dense(36,activation="softmax")
model.add(Dense(36,activation="softmax"))

#yêu cầu Keras build TF model sau scenes

model.compile(loss = "categorical_crossentropy",optimizer="adam", metrics=["accuracy"])

#train neural network
#batch_size=36
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=36, epochs=20, verbose=1)
#Lưu model vào filename

model.save(MODEL_FILENAME)
print("luu model vao model/captcha_model.hdf5")
