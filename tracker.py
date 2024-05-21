#!/usr/bin/env python3

import cv2 as cv
import numpy as np

MAX_TEMPLATE_MATCH = 0.018

max_value = 255
max_value_H = 360//2
low_H = 180 #154 #108
low_S = 0 #14 #9
low_V = 150 #108 #156
high_H = 180
high_S = 80 #205 #87
high_V = 255

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
window_detection_name = 'Object Detection'
min_contour_size_name = 'min contour'

min_contour_size = 300

class Tracker:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.prev_pos = [[-1, -1] for _ in range(20)]
        self.current_pos = [-1, -1]
        self.template_img = None
        self.templates = []

        if not self.cap.isOpened():
            print("Cannot open camera")
        
        try:
            frame = self.read_cap()
            self.frame_shape = frame.shape
        except Exception as e:
            print(e)
    
    @property
    def is_template_captured(self):
        return self.template_img is not None
    
    def read_cap(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            return None
        frame = cv.flip(frame, 1)
        return frame
    
    def capture_template(self, cheese=False):
        try:
            frame = self.read_cap()
            
            if self.template_img is None:
                w, h = self.frame_shape[:2]
                cv.rectangle(frame, (int(h*3/7), int(w*3/7)), (int(h*4/7), int(w*4/7)), (0, 0, 255), 2)
                if cheese:
                    self.template_img = frame[int(w*3/7)+2:int(w*4/7)-1, int(h*3/7)+2:int(h*4/7)-1]
                    for size in [0.9, 1.0, 1.1]:
                        self.templates.append(cv.resize(self.template_img, (int(self.template_img.shape[1]*size), int(self.template_img.shape[0]*size))))
                    self.templates.append(cv.resize(self.template_img, (int(self.template_img.shape[1]*.9), int(self.template_img.shape[0]))))
                    cv.imwrite("./imgs/template.png", self.template_img)
                    cv.imshow('nzomott', self.templates[-1])
                    cv.imshow('template', self.template_img)
                cv.imshow('frame', frame)
                return None
        except Exception as e:
            print(e)
    
    def update(self):
        try:
            if self.template_img is None:
                self.capture_template()
                return None
            
            frame = self.read_cap()

            min_value, _, min_location, _ = cv.minMaxLoc(cv.matchTemplate(frame, self.templates[0], cv.TM_SQDIFF_NORMED))
            for i, img in enumerate(self.templates[1:], 1):
                match_map = cv.matchTemplate(frame, img, cv.TM_SQDIFF_NORMED)
                min_val, _, min_loc, _ =  cv.minMaxLoc(match_map)
                if min_value > min_val:
                    min_value = min_val
                    min_location = min_loc

            self.current_pos = [-1, -1]
            min_val = min_value
            min_loc = min_location
            trows, tcols = self.template_img.shape[:2]
            MPx, MPy = min_loc

            if min_val < MAX_TEMPLATE_MATCH:
                self.current_pos = [(MPx+tcols/2)/self.frame_shape[1], (MPy+trows/2)/self.frame_shape[0]]
                cv.putText(frame, f"{min_val:5f}", (MPx, MPy), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                cv.rectangle(frame, (MPx, MPy), (MPx+tcols,MPy+trows), (0,0,255), 2)

            self.prev_pos.pop()
            self.prev_pos.insert(0, self.current_pos.copy())
            
            cv.imshow('frame', frame)
        except Exception as e:
            print(e)
    
    def __del__(self):
        self.cap.release()
        cv.destroyAllWindows()

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
def on_min_contour_size_trackbar(val):
    global min_contour_size
    min_contour_size = int(val)
    cv.setTrackbarPos(min_contour_size_name, window_detection_name, min_contour_size)

def custom_opening(img: cv.typing.MatLike, kernel: cv.typing.MatLike):
    img = cv.blur(img, (5, 5))
    img = cv.erode(img, kernel)
    img = cv.dilate(img, kernel)
    return img

def custom_threshold(img: cv.typing.MatLike, low: int, high: int):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_threshold = cv.inRange(gray, (low), (high))
    return gray_threshold

def main():
    cv.namedWindow(window_detection_name)
    cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
    cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
    cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
    cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
    cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)
    cv.createTrackbar(min_contour_size_name, window_detection_name, min_contour_size, 2000, on_min_contour_size_trackbar)

    kernel = np.ones((5, 5), np.uint8)
    
    cap = cv.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    ret, frame = cap.read()
    frame_shape = frame.shape
    pixel_num = frame_shape[0] * frame_shape[1]

    on_min_contour_size_trackbar(pixel_num/22**2)

    template_img = None
    small_template = None
    big_template = None
    
    while ret:
        try:
            ret, frame = cap.read()
            
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            
            if template_img is None:
                w, h = frame.shape[:2]
                cv.rectangle(frame, (int(h*3/7), int(w*3/7)), (int(h*4/7), int(w*4/7)), (0, 0, 255), 2)
                if cv.waitKey(1) == ord(' '):
                    template_img = frame[int(w*3/7)+2:int(w*4/7)-1, int(h*3/7)+2:int(h*4/7)-1]
                    template_img2 = cv.Canny(template_img, 85, 170)

                    small_template = cv.resize(template_img, (int(template_img.shape[1]*.8), int(template_img.shape[0]*.8)))
                    big_template = cv.resize(template_img, (int(template_img.shape[1]*1.2), int(template_img.shape[0]*1.2)))
                    cv.imwrite("./imgs/template.png", template_img)
                    cv.imshow('template2', template_img2)
                cv.imshow('frame', frame)
                continue

            match_map = cv.matchTemplate(frame, template_img, cv.TM_SQDIFF_NORMED)
            
            cv.imshow('match_map', match_map)

            min_val, _, min_loc, _ = cv.minMaxLoc(match_map)

            MPx,MPy = min_loc

            trows,tcols = template_img.shape[:2]

            if min_val < 0.18:
                cv.putText(frame, f"{min_val:5f}", (MPx, MPy), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                cv.rectangle(frame, (MPx, MPy), (MPx+tcols,MPy+trows), (0,0,255), 2)
            
            cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break
        except Exception as e:
            print(e)
            break
    
    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
