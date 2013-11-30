
'''This python code performs face tracking. First, the image feed is recieved from the camera. A facial detection algorithm is applied
once in every 5 frames. On detecting the face, a rectangular frame is drawn around the detected face. 
Requires Python + OpenCV'''
import cv2

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 0

def detect_faces(image):
	#print 'detect fn' #
	faces = []
	#detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))
	print detected

	if detected!=[]:
		#print 'face detected' #
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces

if __name__ == "__main__":
	#print 'creating window' #
	cv2.namedWindow("Video")

	capture = cv2.VideoCapture(CAMERA_INDEX)
	#storage = cv.CreateMemStorage()
	cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
	faces = []

	i = 0
	c = -1
	while (c == -1):
		retval, image = capture.read()
		#print 'acq img frm' #

		# Only run the Detection algorithm every 5 frames to improve performance
		if i%5==0:
			#print 'calling detect' #
			faces = detect_faces(image)

		for (x,y,w,h) in faces:
			#print 'drawing rectangle' #
			cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)

		#print 'showing img' #
		cv2.imshow("Video",image)
		#cv.ShowImage("Video", image)
		i += 1
		c = cv2.waitKey(10)
		if(c==27):
			#escape
			break;