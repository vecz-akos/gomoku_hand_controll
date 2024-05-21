#!/usr/bin/env python3

import cv2 as cv

MAX_TEMPLATE_MATCH = 0.018

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
