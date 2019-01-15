import numpy as np 
import matplotlib.pyplot as plt
from scipy import ndimage

def init_depth_map(camera_dims):
  depth_map_list = [[[] for j in range(camera_dims[1])] for i in range(camera_dims[0])]
  return depth_map_list 

def read_data(path):
  file = open(path, "r")
  events = [list(map(float,line.split())) for line in file]
  start_time = events[0][0]
  file.close()
  return events, start_time

def compute_depth(event, depth_map, baseline, focal_length, scan_speed, start_time):
  time, y, x, _ = event
  disparity = x - (time-start_time)*scan_speed
  if disparity != 0:
    depth = (baseline*focal_length) / disparity

  else:
    depth = 100000     #data is captured for a horizontal line hence x
  #print(y, x, depth)
  depth_map[int(x)][int(y)].append(depth)

def compute_final_depth_map(depth_map):
  depth_map_new = [[sum(depth_map[i][j])/ len(depth_map[i][j]) if len(depth_map[i][j])!= 0 else 100000 for j in range(346)] for i in range(260)]
  depth_map_mat = np.array(depth_map_new)
  return depth_map_mat


def plot_depth_map(depth_map):
  plt.title('Depth Map from Structured lighting')
  plt.ylabel('Camera y co-ord')
  plt.xlabel('Camera x co-ord')
  plt.xlim(0, 345)
  plt.ylim(0, 259)
  image = depth_map
  image /= image.max()/255.0 
  image = ndimage.rotate(image, 180) 
  plt.imshow(image)
  plt.colorbar()
  plt.show()

def convert_to_pcd_and_store(depth_map_matrix):
  pass 

def main():
  camera_dims = (260, 346)
  focal_length = 538 # along y-direction
  baseline = 0.015
  scan_speed = 60 # pixels per second coverge
  
  depth_map = init_depth_map(camera_dims)
  
  events, start_time = read_data('Experiment-1/events.txt')
  
  for event in events:
    compute_depth(event, depth_map, baseline, focal_length, scan_speed, start_time)

  depth_map_matrix = compute_final_depth_map(depth_map)
  print(depth_map_matrix)
  plot_depth_map(depth_map_matrix)
  # convert_to_pcd_and_store(depth_map)



if __name__=='__main__':
    main()