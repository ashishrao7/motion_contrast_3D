# This program reads events, calculates the disparity and plots the depth map from the events.txt file in the Experiments folder


import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

bad_depth = 100 # value set to areas which have 0 disparity or areas for which no disparity has been recorded

def init_depth_map(camera_dims):
  ''' 
    Function to define the intial size of the depth map matrix. Based on the size of the camera dimensions.
  '''
  depth_map_list = [[[] for j in range(camera_dims[1])] for i in range(camera_dims[0])]
  return depth_map_list 

def read_data(path):
  '''
    Function to read data from the file containing events
  '''
  file = open(path, "r")
  events = [list(map(float,line.split())) for line in file]
  start_time = events[0][0]
  file.close()
  return events, start_time


def compute_depth(event, depth_map, scan_speed, start_time, focal_length, baseline):
  '''
    Compute depth for each pixel in the depth map. Some pixels could have multiple depths due to multiple activations on the event camera. All the possible values are stored as a list in the 
    corresponding pixel loction. The formula used to calculate depth is the one described in Matsuda et al.
  '''
  
  time, y, x, _ = event #x and y are interchanged because the convention followed is different
  
  # write logic to vet multiscan data, reject initial frame and last frame data
  # get averages of frames 2-5, drop frames 1 and 6
  '''  
    Code goes here
  
  '''
  disparity = x - ((time-start_time)%(260/scan_speed))*scan_speed   #data is captured for a horizontal line hence x is used as opposed to y

  if disparity != 0:
    depth = focal_length * baseline / disparity
  else:
    depth = bad_depth   

  # print("Time Elapsed:{} Disparity :{} Depth:{}".format(time-start_time, disparity, depth))
  # print("new_x:{} new_y:{}".format(new_x, new_y))
  depth_map[int(x)][int(y)].append(depth)

def compute_final_depth_map(depth_map):
  '''
    This function averages depth in each pixel of the depth map to get a single value of depth for each pixel location. The final depth is stored in the depth_map_mat 
    as a numpy array
  '''
  depth_map_new = [[1/(sum(1/np.array(depth_map[i][j]))) / len(depth_map[i][j]) if len(depth_map[i][j])!= 0 else bad_depth for j in range(346)] for i in range(260)]
  depth_map_mat = np.array(depth_map_new)
  return depth_map_mat


def plot_depth_map(depth_map):
  '''
   Plot image of the final depth map numpy array
  '''

  plt.title('Depth Map from Structured lighting')
  plt.ylabel('Camera y co-ord')
  plt.xlabel('Camera x co-ord')
  plt.xlim(0, 345)
  plt.ylim(0, 259)
  image = (depth_map < 100)*depth_map
  image = (image > 15)*depth_map
  image[image==0] = 100
  image = ndimage.rotate(image, 180)  
  plt.imshow(image, cmap ='rainbow')
  plt.colorbar().ax.set_ylabel('depth in cm', rotation=270)
  plt.show()
  print("Plotted Depth Map")
  return image


def convert_to_xyz_and_store(filename, depth_map_matrix):
 
  f = open(filename,"w+")
  for x in tqdm(range(depth_map_matrix.shape[0])):
    for y in range(depth_map_matrix.shape[1]):
      f.write("{}\t{}\t{}\n".format(x, y, depth_map_matrix[x][y]))
  num_lines = sum([1 for line in f])
  f.close()
  print('finished preparing {}. The file has {} lines'.format(filename, num_lines))

def main():

  offset = 0.2 # offset time in seconds

  camera_dims = (260,346)  # Dimensions of a DAVIS346

  scan_speed = 60     # pixels per second coverge , determined by pattern generatad in generator.py

  depth_map = init_depth_map(camera_dims)
  
  events,start_time = read_data('MC3D_new_data/Teddy/events_3.txt')
  #events,start_time = read_data('Experiment-1/events copy.txt')
  #events,start_time = read_data('Teddy_multiscan_6/events_view_1.txt')
  focal_length, baseline = 520, 15
  
  for event in events:
    compute_depth(event, depth_map, scan_speed, start_time+offset, focal_length, baseline)

  depth_map_matrix = compute_final_depth_map(depth_map)

  depth_map = plot_depth_map(depth_map_matrix)

  convert_to_xyz_and_store('3d_points.xyz', depth_map)



if __name__=='__main__':
    main()