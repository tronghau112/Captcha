from PIL import Image
import numpy as np
import imutils
import cv2

def img_open_cv(image):
	open_cv_image = np.array(image)
	open_cv_image = open_cv_image[:,:,::-1].copy()
	return open_cv_image

def alpha_composite(front, back):
    """Alpha composite two RGBA images.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    front -- PIL RGBA Image object
    back -- PIL RGBA Image object

    """
    front = np.asarray(front)
    back = np.asarray(back)
    result = np.empty(front.shape, dtype='float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    falpha = front[alpha] / 255.0
    balpha = back[alpha] / 255.0
    result[alpha] = falpha + balpha * (1 - falpha)
    old_setting = np.seterr(invalid='ignore')
    result[rgb] = (front[rgb] * falpha + back[rgb] * balpha * (1 - falpha)) / result[alpha]
    np.seterr(**old_setting)
    result[alpha] *= 255
    np.clip(result, 0, 255)
    result = result.astype('uint8')
    result = Image.fromarray(result, 'RGBA')
    return result

def composite_with_color(image,color=(255,255,255)):
	#kết hợp 1 hình RGBA với 1 màu của màu đc chỉ định và có cùng kích thước với ảnh gốc
	back = Image.new('RGBA', size=image.size, color=color + (255,))
	return alpha_composite(image, back)

def preprocess_image(image_file):
	image = cv2.imread(image_file)
	#load ảnh và chuyển sang màu gray
	image = img_open_cv(composite_with_color(Image.open(image_file).convert('RGBA')))
	image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	#thêm 1 số padding xq images
	image = cv2.copyMakeBorder(image,8,8,8,8,cv2.BORDER_CONSTANT, value=(255, 0, 0))
	#chuyển đổi images thành đen và trắng

	thresh = cv2.threshold(image,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	#tìm các đường viền (các đốm màu liên tục của pixel) hình ảnh
	contours = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	#print("contours",str(contours))
	contours = contours[0] if imutils.is_cv2() else contours[1]
	output = cv2.merge([image]*3)
	letter_images_regions = []
	for contour in contours:
		#lấy hcn chứa đường viền
		(x,y,w,h) = cv2.boundingRect(contour)

		#ss w vs h để phát hiện chữ cái

		if w/h>1.25:
			#đường viền rộng =>chia 1 nửa thành 2 vùng chữ
			half_width = int(w/2)
			letter_images_regions.append((x,y,half_width,h))
			letter_images_regions.append((x+half_width,y,half_width,h))
		else:
			letter_images_regions.append((x,y,w,h))
	#nếu có nhiều hơn or ít hơn 5 ký tự trong hình => ko trích xuất mà bỏ qua
	if len(letter_images_regions)!=5:
		return ""
	#sắp xết hình ảnh chữ cái đc phát hiện dựa trên toạ độ x xử lý từ trái sang phải
	letter_images_regions = sorted(letter_images_regions,key=lambda x:x[0])
	#mảng ảnh đc xử lý
	letter_images=[]

	#lặp qua các ký tự của ảnh
	for letter_bounding_box in letter_images_regions:
		#lấy toạ độ chữ cái trong hình
		x, y, w, h = letter_bounding_box
		#trích xuất chữ cái từ ảnh gốc với lề 2pixel quanh rìa
		letter_image = image[y - 2:y + h + 2, x - 2:x + w + 2]
		letter_images.append(letter_image)
	return letter_images
