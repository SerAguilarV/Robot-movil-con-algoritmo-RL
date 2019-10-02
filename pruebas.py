import cv2
import numpy as np
# Read image 
img = cv2.imread('line.jpg', cv2.IMREAD_COLOR) # road.png is the filename
# Convert the image to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Find the edges in the image using canny detector
edges = cv2.Canny(gray, 50, 200)
# Detect points that form a line
minLineLength = 1000
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,50,minLineLength,maxLineGap)
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, minLineLength=10, maxLineGap=250)
# Draw lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
# Show result


def mostar(message, img):
    while True:
        cv2.imshow(message, img)
        if cv2.waitKey(1) & 0xFF == ord('\r'): #save on pressing 'y' 
            cv2.destroyAllWindows()
            break


mostar("Result Image", img)