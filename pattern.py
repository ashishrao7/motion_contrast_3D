# This file defines the pattern generator used in the experiment

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
        '''
            Generate moving line whose direction is defined by the variable type
        
        Parameters:
        -----------
            type: <string>
                Defines the direction in which the line has to move

        Return: None
        -------
        '''
        self.video = VideoWriter('./videos/' + type + 'line_pattern_gen_'+str(self.fps)+'_bit.avis', self.fourcc, float(self.fps), (self.width, self.height))
        
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
        
        cv2.destroyAllWindows()
        self.video.release()

class sinusoid_2d(Pattern):
    # generate moving phase patterns 
    def __init__(self, height, width, fps, period, bits_shifted):
        Pattern.__init__(self, height, width, fps)
        self.period = period
        self.pixel_shift = bits_shifted

    def generate_moving_sine(self, type):
        '''
            Generate moving sine-wave whose direction is defined by the variable type
        
        Parameters:
        -----------
            type: <string>
                Defines the direction in which the line has to move

        Return: None
        -------
        '''
        self.video = VideoWriter('./videos/' + type + '_sine_pattern_gen_'+str(self.fps)+'_fps.mkv', self.fourcc, float(self.fps), (self.width, self.height))
        
        if type=='horizontal':
            print('generating video of horizontal sine based phase patterns')
            x = np.arange(self.width)
            y = np.sin(2 * np.pi * x / self.period) 
            
            y += max(y)

            frame = np.array([[y[j]*127 for j in range(346)] for i in range(260)], dtype=np.uint8) # create 2-D array of sine-wave
            
            for _ in range(0, self.width):
                self.video.write(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
                shifted_frame =  np.roll(frame, self.pixel_shift, axis=1)
                frame = shifted_frame 

        if type=='vertical':
            print('generating video of horizontal sine based phase patterns')
            x = np.arange(self.height)
            y = np.sin(2 * np.pi * x / self.period) 
            
            y += max(y)

            frame = np.array([[y[j]*127 for j in range(260)] for i in range(346)], dtype=np.uint8).T # create 2-D array of sine-wave
            
            for _ in range(0, self.height):
                self.video.write(cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB))
                shifted_frame =  np.roll(frame, self.pixel_shift, axis=0)
                frame = shifted_frame 
            
        cv2.destroyAllWindows()
        self.video.release()
            