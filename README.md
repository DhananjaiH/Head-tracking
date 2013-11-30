Head-tracking
=============

This project can perform head tracking and change persepective of viewing 3D objects in Python using OpenCV

[Running these codes requires Python and OpenCV]

File Descriptions:

cam_basic.py : Code that displays an image feed from the camera [Python + OpenCV]

basic_facetrack.py: Code that performs face-tracking using the image feed from a camera [Python + OpenCV]

headtrack.py: Using face-tracking, it can change perception of a 3D wire frame. Requires wireframe3.py to be in the same directory. The motion is very sudden, however, and needs to be scaled to be controllable. [Python + OpenCV + Pygame]

project1_1.py: Performs headtracking in a rendered 3D environment containing 2 cubes. User can move left/right/up/down. This version uses a dynamic origin setting for motion. [Python + OpenCV + VTK]

project1_3.py: Performs headtracking in a rendered 3D environment containing 2 cubes. User can move left/right/up/down and even zoom in/out. This version uses a static origin setting. Motion is based on distance of the user's head from the origin. Motion is also scaled. [Python + OpenCV + VTK]
