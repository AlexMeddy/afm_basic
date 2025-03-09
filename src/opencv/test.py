import cv2
import numpy as np 
from icecream import ic

stream = cv2.VideoCapture('C:\\Users\\alexf\\OneDrive\\Pictures\\Camera Roll\\WIN_20240923_20_37_40_Pro.mp4')
if stream.isOpened():
    print("stream")
    
fps = stream.get(cv2.CAP_PROP_FPS)
ic(fps)
width = int(stream.get(3))
ic(width)
height = int(stream.get(4))
ic(height)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
output = cv2.VideoWriter('output_day.avi', fourcc, 20, (width, height ))
while True:
    ret, frame = stream.read()
    if not ret:
        print("no more stream")
        break
    img = cv2.line(frame, (0,0), (width, height), (300,0,0), 5)
    img = cv2.line(img, (0,height), (width, 0), (300,0,0), 5)
    img = cv2.rectangle(img, (100, 100), (200, 200), (0,267,0), -1)
    img = cv2.circle(img, (300,200), 60, (0,0,255), -1)
    output.write(frame)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
output.release()
cv2.destroyAllWindows()