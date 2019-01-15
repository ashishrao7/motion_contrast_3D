# Motion Contrast 3D Scanning

This repo contains implementation of the motion contrast 3-D Scanning method proposed by <a href="http://compphotolab.northwestern.edu/wordpress/wp-content/uploads/2015/04/dvs_031.pdf"> Matsuda et. al</a>. 

The data in the experiments folder have been collected from a DAVIS346 Camera. The drivers developed by the robotics and perception group were used to collect data from the DAVIS. 

An object is placed on a platform and a moving light source generated in `generator.py` is made to fall on the object. The event camera placed in a stereo configuration with the <a href="http://www.ti.com/tool/DLPLCR4500EVM">light projector</a> records the bending of the incident light and uses this to calculate the depth of the scene.


To understand how events occur in an event based camera, please watch the video at this <a href="https://www.youtube.com/watch?v=kPCZESVfHoQ">link.</a>

Below are the links to different types of Event Cameras,

1. <a href="http://inivation.com/"> DAVIS </a>

2. <a href="https://www.prophesee.ai/"> ATIS </a>
