import cv2
import numpy as np
import pandas as pd
from numpy.linalg import lstsq # to get the form y = mx + b
import time

#The horizon line is nonsense and it always moving
def removeHorizonLine(image, lines):
    for line in lines:
        coords = line[0]
        
    return

#The idea of detecting lane is to check the slope of the line
#OpenCV 0,0 start a top left corner so the slope is flip
#detectLane will merge all similar lines and create best polynomial fit to the curve
#to each other
def detectLane(image, lines):
    # # of lines
    n = lines.shape[0]
    
    #for some reason,HoughLinesP return lines like [[[..]], [[..]]]
    lines = np.reshape(lines, (lines.shape[0], lines.shape[2]))
    
    #https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.lstsq.html
    def getSlopeIntersection(x,y):
        A = np.vstack([x, np.ones(x.shape[0])]).T
        #linsq return y = mx + c
        #this method return (m,c)
        return lstsq(A, y)[0]
    
    #check slope + intersection to see if the line are close to one another
    x = lines[:, [0,2]]
    y = lines[:, [1,3]]
    #horizon = min(y)
    minPixelDifference = 10
    percentSlopeDifference = .1
    slope_intersect = [None]*n

    #similar lines are marked with the same number
    similar_lines = [i for i in range(0,n)]
    #consist of slopes, intersects and the line itself
    final_lines = []
    
    for i in range(0,n):
        if(similar_lines[i] < i):
            #since we already confirm that line[i] is similar to some previous line
            continue
        slope_intersect[i] = getSlopeIntersection(x[i],y[i])        
        #compare the values with other lines
        #while comparing, record the min and max val of x,y coord
        #we want to maximize the line length
        bestYCoords = [y[i][0],y[i][1]]
        averageSlope = slope_intersect[i][0]
        averageIntersect = slope_intersect[i][1]
        count = 1
        for j in range(i+1,n):
            if(similar_lines[j] < j):
                continue            
            if(slope_intersect[j] is None):                
                slope_intersect[j] = getSlopeIntersection(x[j], y[j])

            slopei, intersecti = slope_intersect[i]
            slopej, intersectj = slope_intersect[j]
            if((abs(slopei-slopej) <percentSlopeDifference*slopei) | (abs(intersecti-intersectj) < minPixelDifference)):
                similar_lines[j] = i
                averageSlope+=slope_intersect[j][0]
                averageIntersect+= slope_intersect[j][1]
                count+=1
                if(slopei>0):
                    #(+) slope indicates that y[0] is always smaller than y[1]
                    bestYCoords[0] = y[i][0] if (y[i][0] < y[j][0]) else y[j][0]
                    bestYCoords[1] = y[i][1] if (y[i][1] > y[j][1]) else y[j][1] 
                elif(slopei<0):
                    bestYCoords[0] = y[i][0] if (y[i][0] > y[j][0]) else y[j][0]
                    bestYCoords[1] = y[i][1] if (y[i][1] < y[j][1]) else y[j][1]
                    
        # Construct a new line using the average slope,intersect and best y coordinates y = mx+c => x = (y-c)/m
        averageSlope /=count
        averageIntersect /=count
        x1 =(bestYCoords[0]-averageIntersect)/averageSlope
        if(x1 > 640): x1 = 640
        elif(x1 < 0): x1 = 0
        x2 =(bestYCoords[1]-averageIntersect)/averageSlope
        if(x2 > 640): x2 = 640
        elif(x2 < 0): x2 = 0
        final_lines.append([[averageSlope,averageIntersect],[x1,bestYCoords[0], x2, bestYCoords[1]]])

    
    
    #rid of nonsense since slopes might divide by 0
    #lines = lines[~np.isnan(slopes) & ~np.isinf(slopes),:]
    #slopes = slopes[~np.isnan(slopes) & ~np.isinf(slopes)]

    
    #check for pos or neg slope to move the lines into the correct array
    #rightLines = np.array([lines[i] for i,slope in enumerate(slopes) if slope>0])
    #leftLines = np.array([lines[i] for i,slope in enumerate(slopes) if slope<0])    
    
    return final_lines
        
def draw_lines(originalImage, processedImg, lines, lineColor = [255,255,255], lineWidth=2):
    if(lines is None):
        return
    revampLines = detectLane(processedImg, lines)
    for line in revampLines:
        coords = line[1]
        #print(coords) #[x1,y1,x2,y2]
        try:
            cv2.line(originalImage, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), lineColor, lineWidth)
            cv2.line(processedImg, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), lineColor, lineWidth)
        except Exception as ex:
            print(ex)
            pass
        
##    for line in lines:
##        coords = line[0]
##        #print(coords) [x1,y1,x2,y2]
##        cv2.line(image, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), lineColor, lineWidth)
#get the Region of Interest by
#getting rid of even more redundant info and focus solely on the lane.
#vertices: numpy arrays of the positions of the vertices
def ROI(originalImg, vertices):
    mask = np.zeros_like(originalImg)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(originalImg, mask)
    return masked

def processImg(originalImg):
    #apply cv2 canny edge detection & Gaussian blurring
    processedImg = cv2.cvtColor(originalImg, cv2.COLOR_RGB2GRAY)    
    processedImg = cv2.Canny(processedImg, threshold1 = 50, threshold2 = 150)
    processedImg = cv2.GaussianBlur(processedImg, (5,5),0)

    #get the Region of Interest
    #vertices = np.array([[0,480],[0,225],[150,193],[490,193], [640,225], [640,480]])
    #processedImg = ROI(processedImg, [vertices])

    #detect lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(processedImg, 1, np.pi/180, 100, np.array([]), 20, 15)
    draw_lines(originalImg, processedImg, lines)
    return processedImg

def main():
    img = cv2.imread('fun.png', cv2.IMREAD_COLOR)
    img = cv2.resize(img, (640,480))
    pimg = processImg(img)
    cv2.imshow('original', img)
    cv2.imshow('processed', pimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
