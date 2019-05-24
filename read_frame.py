import cv2
import sys

def cam_init(add):
    camera = cv2.VideoCapture(add)
    if not camera.isOpened():
        print('can not open')
        sys.exit()
    ok, frame = camera.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    length = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
    return camera,ok,frame,length
