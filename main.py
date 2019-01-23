# This program reads events, calculates the disparity and plots the depth map from the events.txt file in the Experiments folder


import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D

bad_depth = 1000 #value set to areas which have 0 disparity or areas for which no disparity has been recorded

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


def compute_depth(event, depth_map, baseline, focal_length, scan_speed, start_time, R, t):
  '''
    Compute depth for each pixel in the depth map. Some pixels could have multiple depths due to multiple activations on the event camera. All the possible values are stored as a list in the 
    corresponding pixel location. The formula used to calculate depth is the one described in Matsuda et al.
  '''
  
  time, y, x, _ = event
  # Do the rotation translation on point x y and compute disparity
  im_coord = np.dot(R.T, np.array(([x],[y],[1])) - t) 
  
  disparity = (time-start_time)*scan_speed #data is captured for a horizontal line hence x is used as opposed to y
 
  if disparity != 0:
    depth = disparity
  else:
    depth = bad_depth   

  depth_map[int(x)][int(y)].append(depth)

def compute_final_depth_map(depth_map):
  '''
    This function averages depth in each pixel of the depth map to get a single value of depth for each pixel location. The final depth is stored in the depth_map_mat 
    as a numpy array
  '''
  depth_map_new = [[(np.array(sum((depth_map[i][j]))))/ len(depth_map[i][j]) if len(depth_map[i][j])!= 0 else bad_depth for j in range(346)] for i in range(260)]
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
  image = (depth_map < 5000)*depth_map
  image = ndimage.rotate(image, 180) 
  plt.imshow(image, cmap='gray')
  plt.colorbar()
  plt.show()


'''def plot_3D_space(depth_mat):
  volume_vector_list = []
  for i in range(260):
    for j in range(346):
      if depth_mat[i][j] < 0:
        volume_vector_list.append(list((i, j, depth_mat[i][j])))
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  xs = np.array(volume_vector_list)[:, 0]
  ys = np.array(volume_vector_list)[:, 1]
  zs = np.array(volume_vector_list)[:, 2]
  ax.scatter(xs, zs, ys)
  plt.show()'''


def convert_to_pcd_and_store(depth_map_matrix):
  pass 

def main():

  camera_dims = (260,346)  # Dimensions of a DAVIS346
  focal_length = 1250  # along y-direction
  baseline = 150    # 15 cm baseline was used in the experiment
  scan_speed = 60     # pixels per second coverge , determined by pattern generatad in generator.py
  
  R = np.array([[ 9.9998744986454580e-01,  1.6931182636345124e-03, 4.7152374222165019e-03], 
                [-2.2544358986445446e-03,  9.9256343510210054e-01, 1.2170762020965244e-01],
                [-4.4741068585167285e-03, -1.2171672296304827e-01, 9.9255479532313740e-01]])
  
  t = np.array([[ 1.2230896982158434e+01], 
                [-1.1936639908933516e+02], 
                [ 9.4031723036298359e+01]])

  depth_map = init_depth_map(camera_dims)
  
  events, start_time = read_data('Experiment-1/events.txt')
  
  for event in events:
    compute_depth(event, depth_map, baseline, focal_length, scan_speed, start_time, R,t)

  depth_map_matrix = compute_final_depth_map(depth_map)

  plot_depth_map(depth_map_matrix)

  # plot_3D_space(depth_map_matrix)
  # convert_to_pcd_and_store(depth_map)



if __name__=='__main__':
    main()