import cv2
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc

class Pattern:
     def __init__(self, height, width, fps):
         self.width = width
         self.height = height 
         self.fps = fps
         self.fourcc = VideoWriter_fourcc(*'MP42')


class Line(Pattern):
    def __init__(self, height, width, fps, thickness):
        Pattern.__init__(self, height, width, fps)
        self.thickness = thickness

    def generate_moving_line(self, type):
        self.video = VideoWriter('./videos/' + type + '_pattern_gen.avi', self.fourcc, float(self.fps), (self.width, self.height))
        
        if type=='vertical':
            print('generating video of vertical line')
            for x_coord in range(0, self.width):
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.line(frame, (x_coord, 0), (x_coord, self.height), (0, 0, 255),self.thickness)
                self.video.write(frame)
        
        if type=='horizontal':
            print('generating video of horizontal line')
            for y_coord in range(0, self.height):
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.line(frame, (0, y_coord), (self.width, y_coord), (0, 0, 255), self.thickness)
                self.video.write(frame)
        
        if type=='tl_diag':
            print('generating line from top left')
            for i in range(0, 2*self.width):
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.line(frame, (0,i), (i,0), (0, 0, 255), self.thickness)
                self.video.write(frame) 
        
        if type=='bl_diag':
            print('generating line from bottom left')
            for i in range(2*self.width):
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.line(frame, (0,self.width-i), (i,self.width), (0, 0, 255), self.thickness)
                self.video.write(frame) 

class sinusoid_2d(Pattern):
    pass