import numpy as np
import cv2
import pyautogui as py
from ldtp import *
from selenium import webdriver



frame = None
roiPts = []
inputMode = False
global paint_open
paint_open = 0
global token
token = 0
global driver
#driver = webdriver.Chrome()

def move (x,y):
    #the function to move the arrow keys with coordinates as input
    if x < 212 :
        print ('R')
        py.press('right')
    elif x > 426 :
        print ('L')
        py.press('left')
    else:
        if y < 160 :
            print ('UP')
            py.press('up')
        elif y > 320 :
            print ('DOWN')
            py.press('down')
        else :
            print ("N")
			
			
def selectROI(event, x, y, flags, param):
	
	global frame, roiPts, inputMode

	
	if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
		roiPts.append((x, y))
		cv2.circle(frame, (x, y), 4, (0, 255, 0), 2)
		cv2.imshow("frame", frame)
#def mouse_movement(frame):

    #print ('x = '+ str(x))
    #print ('y = '+ str(y))
    #move(x,y)
    #mouse controlling actions
    #py.moveTo(int(x*2.5),int(y*2))

def slide_presenter(x,y):
    """
    Layout - a vertical line through the center of screen
         Right side changes the slide
    """
    global token
    token = 1
    if guiexist('*-LibreOfficeImpress'):
        generatemouseevent (100, 200)
        print "Slide Moved"
    else:
        print "office not open"


def scroll_bar(x,y):
    global driver
    if y<200:
        driver.execute_script("window.scrollBy(0,-20);")
    elif y>320:
        driver.execute_script("window.scrollBy(0,20)")
    else:
        print y

def drawing(x,y):
    global paint_open
    if paint_open == 0:
        launchapp('kolourpaint')
        paint_open = 1
    py.dragTo(x,y)



def main():
	
	
	global frame, roiPts, inputMode ,token

	camera = cv2.VideoCapture(0)
	
	cv2.namedWindow("frame")
	cv2.setMouseCallback("frame", selectROI)

	
	termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
	roiBox = None
        li=[]
	
	while True:
		
		(grabbed, frame) = camera.read()
		
		
		if roiBox is not None:
						
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)  # lint:ok

			
			(r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
			pts = np.int0(cv2.cv.BoxPoints(r))
			li.append(pts)
			#print "--------------------"
			#print li[-1][0][0]
    			#print li[-1][0][1]
    			#print "===================="
			
			#coordinates contain the coordinates of the tracked object
                        coordinates = r[0]
                        # x, y contains the coordinates
                        x = int(coordinates[0])
                        y = int(coordinates[1])
                        #py.moveTo(int(x),int(y))
                        if token == 0 and x >= 316:
                            slide_presenter(x,y)
                        elif x<316 :
                            token = 0
                            print x
                        #scroll_bar(x,y)
                        #drawing(x,y)
			
			#draws a circle around the center from x,y
			cv2.circle(frame, (int(x), int(y)), 4, (0, 0, 255), 2)
			
			#cv2.circle(frame,(int(li[-1][0][0]), int(li[-1][0][1])), 4 ,(0,2,0) ,2)
			#cv2.circle(frame,(int(li[-1][1][0]), int(li[-1][1][1])), 4 ,(0,50,0) ,2)
			#cv2.circle(frame,(int(li[-1][2][0]), int(li[-1][2][1])), 4 ,(0,100,0) ,2)
			#cv2.circle(frame,(int(li[-1][3][0]), int(li[-1][3][1])), 4 ,(0,200,0) ,2)
			#draws a colored frame around the object
			cv2.polylines(frame, [pts], True, (255, 0, 0), 2)

		
		cv2.imshow("frame", frame)
		key = cv2.waitKey(1) & 0xFF

		
		# handle if the 'i' key is pressed, then go into ROI
		if key == ord("i") and len(roiPts) < 4:
			
			inputMode = True
			orig = frame.copy()

			while len(roiPts) < 4:
				cv2.imshow("frame", frame)
				cv2.waitKey(0)

			
			roiPts = np.array(roiPts)
			s = roiPts.sum(axis = 1)
			tl = roiPts[np.argmin(s)]
			br = roiPts[np.argmax(s)]

			
			roi = orig[tl[1]:br[1], tl[0]:br[0]]
			roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
			

			
			roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
			roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
			roiBox = (tl[0], tl[1], br[0], br[1])

		# if the 'q' key is pressed, stop the loop
		elif key == ord("q"):
			quit()
			break
		

		

	
	camera.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
