import cv2
import numpy as np
global mouseX, mouseY, savePoint, saveArea
saveArea = savePoint = False
mouseX = mouseY = 0

class DesignArea(object):
    def __init__(self,frame):
        self.detectionAreasDel = self.readAreas(frame)

    def mouseEvent(self,event, x, y, flags, param):
        global mouseX, mouseY, savePoint, saveArea
        if event == cv2.EVENT_LBUTTONDOWN:
            mouseX, mouseY = x, y
            savePoint = True
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            saveArea = True

    def drawAreas(self,frame):
        if self.detectionAreasDel != []:
            for area in self.detectionAreasDel:
                if len(area) > 1:
                    cv2.fillPoly(frame, [np.array(area, np.int32)], (0, 0, 0))
                    cv2.polylines(frame, [np.array(area, np.int32)], True, (0, 0, 0), thickness=3)
        return frame

    def drawAreasConfig(self,frame,detectionAreasDel):
        frameCpy = frame.copy()
        for detectionArea in detectionAreasDel:
            if len(detectionArea) > 1:
                cv2.fillPoly(frameCpy, [np.array(detectionArea, np.int32)], (0, 0, 255))
                cv2.polylines(frameCpy, [np.array(detectionArea, np.int32)], True, (0, 0, 0), thickness=3)
        return cv2.addWeighted(frame, 0.7, frameCpy, 0.3, 0)


    def readAreas(self,frame):
        global mouseX, mouseY, savePoint, saveArea
        windowTitle = 'Please locate detection areas'
        cv2.namedWindow(windowTitle)
        cv2.setMouseCallback(windowTitle, self.mouseEvent)
        detectionAreasDel = []
        detectionArea = []
        while True:
            drawingFrame = frame.copy()
            drawingFrame = self.drawAreasConfig(drawingFrame,detectionAreasDel)
            drawingFrame = self.drawAreasConfig(drawingFrame, [detectionArea])
            cv2.imshow(windowTitle, drawingFrame)
            c = cv2.waitKey(10)
            if c == 27:
                break
            if c & 0xff == ord('c'):
                detectionAreas = []
                detectionArea = []
            if savePoint:
                savePoint = False
                detectionArea.append((mouseX, mouseY))
            if saveArea:
                saveArea = False
                detectionAreasDel.append(detectionArea)
                detectionArea = []

        return detectionAreasDel
