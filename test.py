# this file just contains the assembled operations done on a video 
# that are distributed among different machines aferwards

import numpy as np
import cv2
import json

def test():
    
    videopath = "SampleVideo.mp4"
    i = 0
    cap = cv2.VideoCapture(videopath)
    collector_data = []
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (not ret):
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = np.array(frame, dtype=np.uint8)
        thres,img = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imshow("received_frames", img)
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if (area > 100):    #filter out small contours
                rect = cv2.minAreaRect(cnt)
                boxes.append(cv2.boxPoints(rect).tolist())
        result = {'frame_number': i, 'bounding_boxes' : boxes}
        collector_data.append(result)
        i += 1
        k = cv2.waitKey(1) & 0xFF
        if (k == 27):
            break
    cap.release()
    cv2.destroyAllWindows()

    collector_data.sort(key=lambda frame: frame['frame_number'])
    with open("test_output.json", "w") as file:
        json.dump(collector_data, file, indent=4)

test()