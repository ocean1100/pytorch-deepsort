import cv2
import numpy as np
import os
from DODFunction.utilidades import process_box
from deep_sort.application_util import preprocessing as prep
from deep_sort.application_util import visualization
from deep_sort.deep_sort.detection import Detection as Detection
from deep_sort import generate_detections
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.tracker import Tracker

class track_deepsort(object):

    def __init__(self):

        self.metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.2, 100)
        self.tracker = Tracker(self.metric)
        self.encoder = generate_detections.create_box_encoder(os.path.abspath("deep_sort/resources/networks/mars-small128.ckpt-68577"))

    def return_tracking_id(self, bboxes,frame):
        detections = []
        scores = []
        new_bboxes=[]
        nms_max_overlap = 0.1
        if type(frame) is not np.ndarray:
            imgcv = cv2.imread(frame)
        else: imgcv = frame

        h, w, _ = frame.shape
        thick = int((h + w) // 100)

        for b in bboxes[0]:
            left, top, right, bot, confidence,_,_ = b
            detections.append(np.array([left,top,right-left,bot-top]).astype(np.float64))
            scores.append(confidence)
        detections = np.array(detections)
        if detections.shape[0] == 0 :
            return frame
        scores = np.array(scores)
        features = self.encoder(imgcv, detections.copy())
        detections = [Detection(bbox, score, feature) for bbox,score, feature in zip(detections,scores, features)]# Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = prep.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]
        self.tracker.predict()
        self.tracker.update(detections)
        trackers = self.tracker.tracks

        for track in trackers:
            if not track.is_confirmed() or track.time_since_update > 1:
                    continue
            bbox = track.to_tlbr()
            id_num = str(track.track_id)
            new_bboxes.append((id_num,int(bbox[0]), int(bbox[1]), (int(bbox[2])), int(bbox[3]),track.confidence))
            print(new_bboxes)
        return new_bboxes
