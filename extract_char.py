import os
import os.path
import cv2
import glob
import imutils


IMAGES_FOLDER = "images"
OUTPUT_FOLDER = "output_char"

#lấy ds hình ảnh từ folder images

captcha_images = glob.glob(os.path.join(IMAGES_FOLDER,"*"))
counts = {}

#duyệt tất cả các hình
for (i,captcha_images) in enumerate(captcha_images):
	print("PROCESSING IMAGES: ",i+1)

	filename = os.path.basename(captcha_images)
	captcha_text = os.path.splitext(filename)[0]
	print("CAPTCHA_TEXT",str(captcha_text),"\n")
	letter_images = preprocess_image(captcha_images)
	#lưu mỗi ký tự vào 1 hình khác nhau
	for letter_image,letter_text in zip(letter_images,captcha_text):
		save_path = os.path.join(OUTPUT_FOLDER,letter_text)
		#tạo ra các folder chưa các char nếu chưa có
		if not os.path.exists(save_path):
			os.makedirs(save_path)
		#điền ký tự mỗi ảnh vào file
		count = counts.get(letter_text,1)
		p = os.path.join(save_path,"{}.png".format(str(count).zfill(6)))
		cv2.imwrite(p,letter_image)
		counts[letter_text]=count+1

	
