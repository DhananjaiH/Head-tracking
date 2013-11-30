#headtracking code that performs 3D transformations of a cube using head movement


''''This python code performs headtracking with a 3D wire frame cube. Based on head movement, the object is rotated/scaled. Thus, this code can 
rotate left/right/up/down, as well as zoom in/out.
Requires wireframe3.py to be in the same directory.
Requires Python + OpenCV + Pygame'''

#!/bin/env python

import cv2
import wireframe3 as wireframe
import pygame

HAAR_CASCADE_PATH = "haarcascade_frontalface_alt.xml"
CAMERA_INDEX = 0

key_to_function = {
    0:   (lambda x: x.translateAll('x', -10)),
    1:  (lambda x: x.translateAll('x',  10)),
    2:   (lambda x: x.translateAll('y',  10)),
    3:     (lambda x: x.translateAll('y', -10)),
    4: (lambda x: x.scaleAll(1.1)),
    5:  (lambda x: x.scaleAll( 0.9)),
    6:      (lambda x: x.rotateAll('X',  0.1)),
    7:      (lambda x: x.rotateAll('X', -0.1)),
    8:      (lambda x: x.rotateAll('Y',  0.1)),
    9:      (lambda x: x.rotateAll('Y', -0.1)),
    10:      (lambda x: x.rotateAll('Z',  0.1)),
    11:      (lambda x: x.rotateAll('Z', -0.1)) }

def detect_faces(image):
	faces = []
	detected = cascade.detectMultiScale(image,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if detected!=[]:
		for (x,y,w,h) in detected: #for (x,y,w,h),n in detected:
			faces.append((x,y,w,h))
	return faces

def get_motion(face):
	#yaw is x-axis - horizontal axis
	#pitch is y-axis - depth axis
	#roll is z-axis - vertical axis

	#[0][0] - x, [0][1] - y, [0][2] - w, [0][3] - h

	#w,h are approx constant for U,D,L,R events
	#checking if w,h in range of origin(w,h)+/-5
	if (face[0][2]>(origin[0][2]-5)) and (face[0][2]<(origin[0][2]+5)) and (face[0][3]>(origin[0][3]-5)) and (face[0][3]<(origin[0][3]+5)):
		
		#check x while y is same
		if face[0][1]>(origin[0][1]-5) and face[0][1]<(origin[0][1]+5):
			if face[0][0]>(origin[0][0]-5) and face[0][0]<(origin[0][0]+5):
				#user is in origin location
				print 'origin'
				return 25 #no motion
			else:
				if (face[0][0]-origin[0][0])>0:
					#LEFT motion event - S button
					print 'LEFT'
					return 9
				elif (face[0][0]-origin[0][0])<0:
					#RIGHT motion event - A button
					print 'RIGHT'
					return 8
		else:
			#check y while x is same
			if (face[0][1]-origin[0][1])>0:
				#DOWN motion event - Q button
				print 'DOWN'
				return 6
			elif (face[0][1]-origin[0][1])<0:
				#UP motion event - W button
				print 'UP'
				return 7
	else:
		#possible events: Zoom in, Zoom out
		if (face[0][2]-origin[0][2])>0:
			#ZOOM IN motion event - = button
			print 'ZOOM IN'
			return 4
		elif (face[0][2]-origin[0][2])<0:
			#ZOOM OUT motion event - -button
			print 'ZOOM OUT'
			return 5

class ProjectionViewer:
    """ Displays 3D objects on a Pygame screen """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)

        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4

    def addWireframe(self, name, wireframe):
        """ Add a named wireframe object. """

        self.wireframes[name] = wireframe

    def run(self):
        """ Create a pygame screen until it is closed. """

        running = True
        while running:
        	retval, image = capture.read()

        	global i, ctr, origin, faces

        	# Only run the Detection algorithm every 3 frames to improve performance
        	if i%3==0:
        		faces = detect_faces(image)
        		print 'current coords',faces
        		ctr += 1

        	for (x,y,w,h) in faces:
        		cv2.cv.Rectangle(cv2.cv.fromarray(image), (x,y), (x+w,y+h), 255)

        	if ctr==20:
        		#approx 3 secs of config time
        		origin = faces
        		print 'origin is ',origin

        	if origin!=[] and faces!=[]:
        		dir = get_motion(faces)
        		print 'direction vector',dir
        		if dir in key_to_function:
        			key_to_function[dir](self)

        	cv2.imshow("Video",image)
        	i += 1
        	c = cv2.waitKey(10)

        	if c==27:
        		break
        	
        	self.display()
        	pygame.display.flip()
        
    def display(self):
        """ Draw the wireframes on the screen. """

        self.screen.fill(self.background)

        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for edge in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, (edge.start.x, edge.start.y), (edge.stop.x, edge.stop.y), 1)

            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node.x), int(node.y)), self.nodeRadius, 0)

    def translateAll(self, axis, d):
        """ Translate all wireframes along a given axis by d units. """

        for wireframe in self.wireframes.itervalues():
            wireframe.translate(axis, d)

    def scaleAll(self, scale):
        """ Scale all wireframes by a given scale, centred on the centre of the screen. """

        centre_x = self.width/2
        centre_y = self.height/2

        for wireframe in self.wireframes.itervalues():
            wireframe.scale((centre_x, centre_y), scale)

    def rotateAll(self, axis, theta):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """

        rotateFunction = 'rotate' + axis

        for wireframe in self.wireframes.itervalues():
            centre = wireframe.findCentre()
            getattr(wireframe, rotateFunction)(centre, theta)

if __name__ == '__main__':
    pv = ProjectionViewer(640, 480)

    cube = wireframe.Wireframe()
    cube.addNodes([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
    cube.addEdges([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])

    cv2.namedWindow("Video",400)

    capture = cv2.VideoCapture(CAMERA_INDEX)
    cascade = cv2.CascadeClassifier(HAAR_CASCADE_PATH)
    faces = [] #var that stores face rect coords
    origin = [] #var that will store the origin coords

    i = 0
    c = -1
    ctr = 0 #for counting the no. of detections
    
    pv.addWireframe('cube', cube)
    pv.run()