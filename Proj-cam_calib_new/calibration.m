% Projector-Camera Stereo calibration parameters:

% Intrinsic parameters of camera:
fc_left = [ 1249.648684 1234.768910 ]; % Focal Length
cc_left = [ 417.646695 379.608321 ]; % Principal point
alpha_c_left = [ 0.000000 ]; % Skew
kc_left = [ -0.299573 6.190693 -0.005582 -0.010924 0.000000 ]; % Distortion

% Intrinsic parameters of projector:
fc_right = [ 2022.319155 1881.202963 ]; % Focal Length
cc_right = [ 379.448877 468.985661 ]; % Principal point
alpha_c_right = [ 0.000000 ]; % Skew
kc_right = [ 0.324640 2.959880 0.091444 -0.069673 0.000000 ]; % Distortion

% Extrinsic parameters (position of projector wrt camera):
om = [ -0.122015 0.004606 -0.001979 ]; % Rotation vector
T = [ 12.230897 -119.366399 94.031723 ]; % Translation vector
