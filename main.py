# This program reads events, calculates the disparity and plots the depth map from the events.txt file in the Experiments folder


import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage
from mpl_toolkits.mplot3d import Axes3D

bad_depth = 500 #value set to areas which have 0 disparity or areas for which no disparity has been recorded

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
    corresponding pixel loction. The formula used to calculate depth is the one described in Matsuda et al.
  '''
  
  time, y, x, _ = event #x and y are interchanged because the convention followed is different
  # Do the rotation translation on point x y and compute disparity
  im_coord = np.dot(R.T, np.array(([x],[y],[1])) - t) + t 
  
  disparity = 150*im_coord[0]/(im_coord[2]*focal_length) - (time-start_time)*scan_speed #data is captured for a horizontal line hence x is used as opposed to y

  if disparity != 0:
    depth = focal_length * baseline/disparity
  else:
    depth = bad_depth   

  # print("Time Elapsed:{} Disparity :{} Depth:{}".format(time-start_time, disparity, depth))
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
  image = (depth_map < 800)*depth_map
  image = (image > 0)*image
  image = ndimage.rotate(image, 180) 
  plt.imshow(image)
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
  focal_length = 450 # along y-direction
    # 15 cm baseline was used in the experiment
  scan_speed = 60     # pixels per second coverge , determined by pattern generatad in generator.py
  
  R = np.array([[0.9910483601989318, -0.001257937490197782, -0.1334974357067545],
                [-0.05010500313601597, 0.9233539397380011, -0.3806665084178691 ],
                [0.1237442378769538, 0.3839478083849191, 0.9150253788986781]])
  
  t = np.array([[2.100388684052633],
               [-54.19534011618826],
               [-35.31909568783666]])

  baseline = np.linalg.norm(t)
  print('The baseline is {}'.format(baseline))

  depth_map = init_depth_map(camera_dims)
  
  events, start_time = read_data('Experiment-1/events copy.txt')
  
  for event in events:
    compute_depth(event, depth_map, baseline, focal_length, scan_speed, start_time, R,t)

  depth_map_matrix = compute_final_depth_map(depth_map)

  plot_depth_map(depth_map_matrix)

  # plot_3D_space(depth_map_matrix)
  # convert_to_pcd_and_store(depth_map)



if __name__=='__main__':
    main()