import cv2
import imutils

def resize_image(image,width,height):

	(h,w) = image.shape[:2]

	#nếu chiều rộng > chiều cao => thay đổi kích thước
	if w>h:
		image=imutils.resize(image,width=width)
	# ngược lại thì thay đổi kích thước dọc theo chiều cao
	else:
		image=imutils.resize(image,height=height)
	#xác định các giá trị đệm để có kích thước đích

	padW = int((width - image.shape[1])/2.0)
	padH = int((height-image.shape[0])/2.0)

	image = cv2.copyMakeBorder(image,padH,padH,padW,padW,cv2.BORDER_REPLICATE)
	image=cv2.resize(image,(width,height))

	return image
