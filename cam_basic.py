
'''This python code simply gets image feed from the webcam. 
Requires Python + OpenCV'''
import cv

cv.NamedWindow("preview", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

def repeat():

    frame = cv.QueryFrame(capture)
    cv.ShowImage("preview", frame)
    cv.WaitKey(10)


while True:
    repeat()