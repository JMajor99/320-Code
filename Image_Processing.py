import cv2
import picamera2

cap = picamera2.Picamera2() # all images the pi can capture
config = cap.create_video_configuration(main={"format":'XRGB8888',"size":(820,616)}) # Setting the resolution (croping size image). Lower is faster processing
cap.configure(config) # 
cap.set_controls({"ExposureTime": 100000, "AnalogueGain": 1.0, "ColourGains": (1.4,1.5)}) # IMPORTANT, gain of certian colours

cap.start()
while(1):
    frame = cap.capture_array()
    # convert from RGBX to RGB
    frame_rgb = frame[:, :, :3]
    
    # Frame = cv2.rotate(frame, cv2.ROTATE_180)
    # hsv_frame = cv2.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Convert from BGR to HSDV colourspace
    # cvs.imwrite("frame00.png", frame_rgb)
    
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

cap.close()
cv2.destroyAllWindows()
