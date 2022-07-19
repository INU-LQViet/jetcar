import cv2 
import os
import numpy as np
from utils import ArducamUtils


class MyCamera(object):
    def __init__(self, device = 0, width = -1, height = -1,
     file_type  = ".jpg", photo_string= "stream_photo"):
        self.cap = cv2.VideoCapture(device, cv2.CAP_V4L2)
        self.arducam_utils = ArducamUtils(device)
        # turn off RGB conversion
        if self.arducam_utils.convert2rgb == 0:
            self.cap.set(cv2.CAP_PROP_CONVERT_RGB, self.arducam_utils.convert2rgb)
        # set width
        if width != -1:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        # set height
        if height != -1:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.file_type = file_type 
        self.photo_string = photo_string 
        
    def get_framesize(self):
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return (width, height)

    def close_camera(self):
        self.cap.release()
        self.cap = None

    def get_frame(self):
        ret, frame0 = self.cap.read()
        if not ret:
            return None
        frame = self.arducam_utils.convert(frame0)
        jpeg = cv2.imencode(self.file_type, frame)[1]
        data_encode = np.array(jpeg)
        self.previous_frame = jpeg
        return data_encode.tobytes()