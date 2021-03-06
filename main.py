#######################################################################################
#This is an implementation of the Motion Contrast 3D method
# Author: Ashish Rao M
# email: ashish.rao.m@gmail.com
#######################################################################################
import numpy as np 
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import os

bad_depth = 100 # value set to areas which have 0 disparity or areas for which no disparity has been recorded

def init_depth_map(camera_dims):
  ''' 
    Function to define the intial size of the depth map matrix. Based on the size of the camera dimensions.

    Parameters:
    -----------
    camera_dims: <int tuple>
      Species resolution of the camera the event data comes from 

    Return:
    -------
    depth_map_list: <np.array of dimensions cam_width x cam_height with each index containing a list>
      Matrix of said dimensions containing empty lists at all positions
  '''
  depth_map_list = [[[] for j in range(camera_dims[1])] for i in range(camera_dims[0])]
  return depth_map_list 

def read_data(path):
  '''
    Function to read data from the file containing events

    Parameters:
    -----------
    path: <string>
      The location of data to be read from
    
    Return:
    -------
    events: <list>
      A list of events read from the file 
  '''
  file = open(path, "r")
  events = [list(map(float,line.split())) for line in file]
  start_time = events[0][0]
  file.close()
  return events, start_time

def compute_depth_raster_scanning(event, depth_map, scan_speed, start_time, focal_length, baseline, camera_dims):
  '''
  Function to compute depth using raster scanning principles. Code is still experimental 
  '''
  
  time, y, x, _ = event #x and y are interchanged because the convention followed is different
  if scan_speed*time > camera_dims[1]:
    start_time = time
  
  disparity = y - ((time-start_time)%(camera_dims[1]/scan_speed))*scan_speed   #horizontal stereo pair used here 
  if disparity != 0:
    depth = focal_length * baseline / disparity
  else:
    depth = bad_depth   
  depth_map[int(x)][int(y)].append(depth)
  return start_time, x


def compute_depth_line_scanning(event, depth_map, scan_speed, start_time, focal_length, baseline):
  '''
    The computation of depth using triangulation method for the line scanner

    ---------
    Parameters:
    -----------
    event: <list>
      A list containing the event -> timestamp, x, y, polarity 

    depth_map: <np.array of dimensions cam_width x cam_height with each index containing a list>
      Matrix of said dimensions containing empty lists at all positions

    start_time: <float>
      The start time of the experiment   

    baseline: <float> 
     The baseline separation of the stereo setup
    
    scan_speed: <int> 
      Speed in pixels per second at which the pattern moves

    focal_length : <float>
      The focal length of the camera
    
    Return:
    -------
    depth_map: <np.array containng lists>
      A matrix of camera dimensions containing a single element list of depths corresponding to that location of the camera
  '''
  time, y, x, _ = event # x and y are interchanged because the convention followed is different
  
  ######################################### for raster scanning #########################
  # write logic to vet multiscan data, reject initial frame and last frame data
  # get averages of frames 2-5, drop frames 1 and 6
  ########################################################################################
  disparity = x - ((time-start_time)%(260/scan_speed))*scan_speed   #data is captured for a horizontal line hence x is used as opposed to y
  if disparity != 0:
    depth = focal_length * baseline / disparity
  else:
    depth = bad_depth   
  # print("Time Elapsed:{} Disparity :{} Depth:{}".format(time-start_time, disparity, depth))
  depth_map[int(x)][int(y)].append(depth)

def compute_final_depth_map(depth_map):
  '''
    This function averages depth in each pixel of the depth map to get a single value of depth for each pixel location. The final depth is stored in the depth_map_mat 
    as a numpy array

    Parameters:
    ----------
    depth_map_list: <np.array of dimensions cam_width x cam_height with each index containing a list>
      Matrix of said dimensions containing empty lists at all positions

    depth_map: <numpy array, size camera dimensions>
      Numpy array of depth values at each position
  '''
  depth_map_new = [[1/(sum(1/np.array(depth_map[i][j]))) / len(depth_map[i][j]) if len(depth_map[i][j])!= 0 else bad_depth for j in range(346)] for i in range(260)]
  depth_map_mat = np.array(depth_map_new)
  return depth_map_mat


def plot_depth_map(depth_map):
  '''
   Plot image of the final depth map numpy array
   Parameters:
    -----------
    depth_map: <numpy array, size camera dimensions>
      Numpy array of depth values at each position
    
    Return:
    -------
    image: <numpy array, size camera dimensions>
      Final processed depth map

  '''

  plt.title('Depth Map from Structured lighting')
  plt.ylabel('Camera y co-ord')
  plt.xlabel('Camera x co-ord')
  plt.xlim(0, 345)
  plt.ylim(0, 259)

  image = (depth_map < 100)*depth_map
  image = (image > 15)*depth_map
  image[image==0] = 100
  image = image.astype(np.uint8)
  
  #image = cv2.medianBlur(image, 3)
  #image = cv2.bilateralFilter(image, 9, 10, 10)

  image = ndimage.rotate(image, 180)  
  plt.imshow(image, cmap ='jet')
  plt.colorbar().ax.set_ylabel('depth in cm', rotation=270)
  plt.show()
  print("Plotted Depth Map")
  return image

def make_video(image_folder):  
  '''
  Make video from images. 

  Parameters:
  ----------
  image_folder: <string>
    directory of the folder containing the images
  '''
  video_name = 'videos/MC3D_moving.avi'

  images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
  frame = cv2.imread(os.path.join(image_folder, images[0]))
  height, width, layers = frame.shape
  video = cv2.VideoWriter(video_name, 0, 30, (width,height))
  for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))
  cv2.destroyAllWindows()
  video.release()

def convert_to_xyz_and_store(filename, depth_map_matrix):
  '''
    Convert the depth map values to xyz file and store in the current directory
    
    Parameters:
    -----------
    filename: <string> 
      Name of the file to be saved

    depth_map_matrix: <np.array>
      Matrix containing depth values at all position of the image
  '''
  f = open(filename,"w+")
  for x in range(depth_map_matrix.shape[0]):
    for y in range(depth_map_matrix.shape[1]):
      if depth_map_matrix[x][y]<bad_depth:
        f.write("{}\t{}\t{}\n".format(x, y, depth_map_matrix[x][y]))
  num_lines = np.sum([1 for line in f])
  f.close()
  print('finished preparing {}. It has {} lines.'.format(filename, num_lines))

def main_line_scanning():
  offset = 0.1 
  # offset time in seconds, Has to be changed and adjusted trial and error for every experimental reading this code is run on  
  # because of manually method of starting light pattern and recording data from the dvs(there is no stero sync). Usually values between -1 and 1

  focal_length, baseline = 510, 15  #adjusted based on experimental setup
  obj =  'Hand' # Can be changed to 'Hand', 'Teddy', 'Swan', etc (any of the directory names of the MC3D_new_data directory)
  
  camera_dims = (260,346)  # Dimensions of a DAVIS346
  scan_speed = 60     # pixels per second coverge , determined by pattern generatad in generator.py
  depth_map = init_depth_map(camera_dims)
  events,start_time = read_data('MC3D_new_data/' + obj + '/events_1.txt')

  for event in events:
    compute_depth_line_scanning(event, depth_map, scan_speed, start_time+offset, focal_length, baseline)

  depth_map_matrix = compute_final_depth_map(depth_map)
  depth_map = plot_depth_map(depth_map_matrix)
  convert_to_xyz_and_store(obj + '_points.xyz', depth_map)

def main_raster_scanning():
  '''
  Experimental method. Work in progress......
  '''
  offset = 0.5 # Should be between 0 and 1/60 seconds
  camera_dims = (260,346)  # Dimensions of a DAVIS346
  scan_speed = 1/(60*camera_dims[0])     # raster scan speed of the projector
  depth_map = init_depth_map(camera_dims)
  
  events,start_time = read_data('') #event data with a white image pattern overlaid on the object to be scanned
  start_time += offset
  focal_length, baseline = 410, 15
  
  row_counter, frame = 0, 0 #maintain row count for raster scanning, frame number of video image naming
  for event in events:   
    if event[0]-start_time >= 1/60: 
      start_time = event[0]
      depth_map_matrix = compute_final_depth_map(depth_map)
      depth_image = plot_depth_map(depth_map_matrix)
      cv2.imwrite('MC3D_video_mode/' + str(frame).zfill(3)+'.png', depth_image)
      depth_map = init_depth_map(camera_dims)
      frame+=1

    else:
      start_time, row_counter = compute_depth_raster_scanning(event, depth_map, scan_speed, start_time, focal_length, baseline, camera_dims)
      
    #frame splitting issues exist in this routine above look into correcting it
    make_video('MC3D_video_mode/')




if __name__=='__main__':
    main_line_scanning()