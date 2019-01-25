% Projector-Camera Stereo calibration parameters:

% Intrinsic parameters of camera:
fc_left = [ 216.209526 191.092868 ]; % Focal Length
cc_left = [ 159.932681 122.725949 ]; % Principal point
alpha_c_left = [ 0.000000 ]; % Skew
kc_left = [ 0.489428 -4.595708 0.105252 0.020326 0.000000 ]; % Distortion

% Intrinsic parameters of projector:
fc_right = [ 638.132876 588.991972 ]; % Focal Length
cc_right = [ 521.466459 587.144121 ]; % Principal point
alpha_c_right = [ 0.000000 ]; % Skew
kc_right = [ 0.061772 -0.172705 0.023018 -0.008527 0.000000 ]; % Distortion

% Extrinsic parameters (position of projector wrt camera):
om = [ 0.354051 -0.104306 -0.021666 ]; % Rotation vector
T = [ 3.598423 -53.674619 -35.238142 ]; % Translation vector
