# File: cube.py
'''
This python code performs Headtracking in 3D environment - version 2.
Performs movement in up/down/left/righ/zoom in/zoom out.
This version uses a distance algorithm. Motion is based on the displacement from the ORIGIN.
Requires Python + OpenCV + VTK'''

# import vtk python module
#headtracking code that performs 3D transformations of a cube using head movement
#uses facetrack.py + displayWireframe3.py

#!/bin/env python
import vtk
import time
from numpy import *
import cv2
import pygame

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 0
matrix = [[[0 for x in xrange(4)] for x in xrange(1)] for x in xrange(20)]
matrix1 = [[[0 for x in xrange(4)] for x in xrange(1)] for x in xrange(1)]
matrix1[0][0][0] = 0
matrix1[0][0][1] = 0
matrix1[0][0][2] = 0
matrix1[0][0][3] = 0
a = 0

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("MiddleButtonPressEvent",self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent",self.middleButtonReleaseEvent)
 
    def middleButtonPressEvent(self,obj,event):
        print "Middle Button pressed"
        self.OnMiddleButtonDown()
        return
 
    def middleButtonReleaseEvent(self,obj,event):
        print "Middle Button released"
        self.OnMiddleButtonUp()
        return

# create polygonal cube geometry
#   here a procedural source object is used,
#   a source can also be, e.g., a file reader
# create polygonal cube geometry
#   here a procedural source object is used,
#   a source can also be, e.g., a file reader
cube = vtk.vtkCubeSource()
cube.SetBounds(-1,1,-1,1,-1,1)
cube.SetCenter(0,0,-3)

# map to graphics library
#   a mapper is the interface between the visualization pipeline
#   and the graphics model
mapper = vtk.vtkPolyDataMapper()
mapper.SetInput(cube.GetOutput()); # connect source and mapper

# an actor represent what we see in the scene,
# it coordinates the geometry, its properties, and its transformation
aCube = vtk.vtkActor()
aCube.SetMapper(mapper);
aCube.GetProperty().SetColor(0,1,0); # cube color green

#cube 2

cube2 = vtk.vtkCubeSource()
cube2.SetBounds(-0.6,0.6,-0.6,0.6,-0.6,0.6)
cube2.SetCenter(0,0,0)

# map to graphics library
#   a mapper is the interface between the visualization pipeline
#   and the graphics model
mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInput(cube2.GetOutput()); # connect source and mapper

# an actor represent what we see in the scene,
# it coordinates the geometry, its properties, and its transformation
bCube = vtk.vtkActor()
bCube.SetMapper(mapper2);
bCube.GetProperty().SetColor(0,1,1); # cube color
# a renderer and render window
ren1 = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1);


#interactor = vtk.vtkRenderWindowInteractor()
#interactor.SetInteractorStyle(MyInteractorStyle())
#interactor.SetRenderWindow(renWin)
#interactor.Initialize()

# an interactor
#iren = vtk.vtkRenderWindowInteractor()
#iren.SetRenderWindow(renWin);

# add the actor to the scene
ren1.AddActor(aCube);
ren1.AddActor(bCube);
ren1.SetBackground(1,1,1); # Background color white
i=0

## ----------- MORE CAMERA SETTINGS -----------------
## Initialize camera
cam = ren1.GetActiveCamera()
cam.SetFocalPoint(1,0,0)
cam.SetViewUp(0.,1.,0.);

## This is added so that it gives time to set
## no border in the OpenGL window and other stuff
## like minimizing other windows. 

renWin.Render()
t = 0.0
i = 0
j=0



def detect_faces(image):
    faces = []
    detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

    if detected!=[]:
        for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces


def get_motion(f_x,f_y,f_wid):
    #yaw is x-axis - horizontal axis
    #pitch is y-axis - depth axis
    #roll is z-axis - vertical axis

    #[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h
    
    #w,h are approx constant for U,D,L,R events
    #checking if w,h in range of origin(w,h)+/-5
    if (f_wid>(o_wid-20)) and (f_wid<(o_wid+20)):
        
        #check x while y is same
    
        
        if f_y>(o_y-5) and f_y<(o_y+5):
            if f_x>(o_x-5) and f_x<(o_x+5):
                #user is in origin location
                #print 'origin'
                return 25 #no motion
            else:
                if (f_x-o_x)>0:
                    #LEFT motion event - S button
                    #print 'LEFT', a
                    return 0
                elif (f_x-o_x)<0:
                    #RIGHT motion event - A button
                    #print 'RIGHT', f_x-o_x
                    return 1
        else:
            #check y while x is same
            if (f_y-o_y)>0:
                #DOWN motion event - Q button
                #print 'DOWN'
                return 2
            elif (f_y-o_y)<0:
                #UP motion event - W button
                #print 'UP'
                return 3
    else:
        #possible events: Zoom in, Zoom out
        if (f_wid-o_wid)>0:
            #ZOOM IN motion event - = button
            #print 'dir-ZOOM IN'
            return 4
        elif (f_wid-o_wid)<0:
            #ZOOM OUT motion event - -button
            #print 'dir-ZOOM OUT'
            return 5

'''
while 1:
    renWin.Render();
    if i in range(0,10): 
        camera=vtk.vtkCamera();
        camera.SetPosition(i, 0,100);
        camera.SetFocalPoint(255, 255, 0);
        ren1.SetActiveCamera(camera);
        #ren1.ResetCameraClippingRange()

        time.sleep(1);

# begin mouse interaction
#iren.Start();
'''
cam.SetPosition(5,5,5)
#time.sleep(0.1)
cam.SetFocalPoint(0,0,0)
if __name__ == '__main__':


    
    cv2.namedWindow("Video",400)

    capture = cv2.VideoCapture(CAMERA_INDEX)
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    faces = [] #var that stores face rect coords
    origin = [] #var that will store the origin coords
    o_x = 0
    o_y = 0
    o_wid = 0
    a = 0

    i = 0
    c = -1
    ctr = 0 #for counting the no. of detections
    t = 0
    running = True

    while running:
        retval, image = capture.read()

        #global i, ctr, origin, faces, t, o_x, o_y, o_wid, a

        # Only run the Detection algorithm every 3 frames to improve performance
        for (x,y,w,h) in matrix1[0]:
            cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 0)
        if i%3==0:
            faces = detect_faces(image)
            #print 'current coords',faces
                
        if faces != []:
            if ctr < 20:
                matrix [ctr][0][0] = faces[0][0]
                matrix [ctr][0][1] = faces[0][1]
                matrix [ctr][0][2] = faces[0][2]
                matrix [ctr][0][3] = faces[0][3]
                #print 'currentvalue and frame:', matrix [ctr], ctr
                ctr += 1
            if ctr==20:
                #approx 3 secs of config time
                for t in xrange(ctr):
                    matrix1 [0][0][0] = matrix1[0][0][0] + matrix[t][0][0]
                    matrix1 [0][0][1] = matrix1[0][0][1] + matrix[t][0][1]
                    matrix1 [0][0][2] = matrix1[0][0][2] + matrix[t][0][2]
                    matrix1 [0][0][3] = matrix1[0][0][3] + matrix[t][0][3]
                matrix1[0][0][0]= matrix1[0][0][0]/20
                matrix1[0][0][1]= matrix1[0][0][1]/20
                matrix1[0][0][2]= matrix1[0][0][2]/20
                matrix1[0][0][3]= matrix1[0][0][3]/20
                o_x = (matrix1[0][0][0] + matrix1[0][0][2])/2
                o_y = (matrix1[0][0][1] + matrix1[0][0][3])/2
                o_wid = matrix1[0][0][2]
                #print 'origin is ',matrix1, o_x, o_y, o_wid
                ctr += 1

        for (x,y,w,h) in matrix1[0]:
            cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 0)

        for (x,y,w,h) in faces:
            cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)



        if o_x!= 0 and faces!=[]:
            f_x = (faces[0][0] + faces[0][2])/2
            f_y = (faces[0][1] + faces[0][3])/2
            f_wid = faces[0][2]
            dir = get_motion(f_x,f_y,f_wid)
            if (dir == 0 or dir == 1):
                a = (f_x-o_x)/float(10)
                round(a)
                cam.Azimuth(-a)
            elif (dir == 2 or dir == 3):
                a = (f_y-o_y)/float(10)
                round(a)
                cam.Elevation(-a)

            if (f_wid-o_wid>7.5 or o_wid-f_wid>7.5):
                #zoom in or zoom out
                #a = f_wid/o_wid
                a = 0
                if(f_wid-o_wid>7.5):
                    #zoom in case
                    a=1.01
                    #print 'zooming in'
                elif(o_wid-f_wid>7.5):
                    #zoom out case
                    a=0.99
                    #print 'zooming out'
                cam.Zoom(a)
            else:
                #print 'nothing.'
                a=0
            #print 'direction vector',dir
            #if dir in key_to_function:
                #key_to_function[dir](self)
            #print 'value:', a
        ## --------  THE MAIN FRAME LOOP ----------------------
        # Loop while: rotating the camera and modify
        # node coordinates

    

            ## This recomputes the clipping plane.
        ## Otherwise, since the camera
        ## is rotating, some objects may disappear
        ren1.ResetCameraClippingRange()
        
        #x,y = interactor.GetEventPosition()
        #print 'mouse position:',x,', ',y
        #interactor.Enable()
        #interactor.Start()
    

    ## Update camera
   

        
        #cam.Roll(i)
        
        #print 'App:', cam.GetViewShear()
        #cam.SetViewUp(0.,i,0.);


        
        renWin.Render()

        # render an image (lights and cameras are created automatically)
        

        cv2.imshow("Video",image)
        i += 1
        if i>100:
            i=0
        c = cv2.waitKey(10)

        if c==27:
            break

