from pyzbar.pyzbar import decode
from imutils.video import VideoStream
import time
from PIL import Image 
import cv2
import imutils	
RASP=False #rasp

if RASP :
	print("[INFO] starting video stream...")
	vs = VideoStream(usePiCamera=False).start()
	if vs:
		time.sleep(1.0)
		print('[INFO]The camera is ready!')

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		qrcodes = decode(frame)
		
		for qrcode in qrcodes:
			(x, y, w, h) = qrcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			qrcodeData = qrcode.data.decode("utf-8")
			qrcodeType = qrcode.type
			text = "{} ({})".format(qrcodeData, qrcodeType)
			cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
		print('QR code ddata is: '+qrcodeData)
	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	print("[INFO] Bye Bye...")
	cv2.destroyAllWindows()
	vs.stop()
else:
	print("[INFO] starting video stream...")
	cap = cv2.VideoCapture(0)
	if cap:
		time.sleep(1.0)
		print('[INFO]The camera is ready!')
	while True:
		ret, frame = cap.read()
		frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
		#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		qrcodes = decode(frame)
		
		for qrcode in qrcodes:
			(x, y, w, h) = qrcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
			qrcodeData = qrcode.data.decode("utf-8")
			qrcodeType = qrcode.type
			text = "{} ({})".format(qrcodeData, qrcodeType)
			cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				
		cv2.imshow("Barcode Scanner", frame)
		key = cv2.waitKey(1) & 0xFF
		try:
			print('QR code ddata is: '+qrcodeData)
		except:
			print("An exception occurred")
	
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	print("[INFO] Bye Bye...")
	cv2.destroyAllWindows()
	vs.stop()
