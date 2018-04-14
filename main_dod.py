
import os
from Detection_pyTorch.main_module import Network
from deep_sort.main_module import track_deepsort
from DODFunction.saves import saves
import cv2

class task_get_detections(object):

    def __init__(self,cfgfile, weightfile,frame,batch_size):
        self.net = Network(cfgfile, weightfile,frame, conf_thresh=0.5, nms_thresh=0.4, batch_size=batch_size, gpus=1)

    def Detection(self,batch_frame):
        bboxes = self.net.return_predict(batch_frame)
        return bboxes

class task_get_tracking(object):

    def __init__(self,):
        self.tracking = track_deepsort()

    def track(self,bboxes,frame):
        frame  = self.tracking.return_tracking_id(bboxes,frame)
        return frame

save = saves('/home/guilherme/Python/Videos/2_minutos_v2.mp4', # 'camera' para real time
            'newera',#nome loja newera ou racing. Somenta quando primeiro arg é camera
            '1', #Canal de acesso a camera 1 a 8
            '2', #resolução 1 high e 2 low
            600) # Tempo de particionamento dos videos 
_, frame = save.camera.read()
h, w, _ = frame.shape
thick = int((h + w) // 100)
Detection = task_get_detections('Detection_pyTorch/cfg/yolo_person.cfg','Detection_pyTorch/backup/yolo_person.weights',frame.shape,batch_size=1)
Tracking = task_get_tracking()
n=0
while(save.camera.isOpened()):
    _, frame = save.camera.read()
    choice = cv2.waitKey(1)
    if n<=150:
        n+=1
        continue
    save.verify()
    bboxes = Detection.Detection(frame) #Saida [x,y,x2,y2,confidence, _,_]
    new_bboxes = Tracking.track(bboxes,frame)#Saida [id_num,x,y,x2,y2,confidence, _,_]
    for bbox in new_bboxes:
        cv2.rectangle(frame, (bbox[1], bbox[2]), (bbox[3], bbox[4]), (0,255,0), thick//3)
        cv2.putText(frame,bbox[0] ,((bbox[1]), (bbox[2]) - 12),0, 1e-3 * h, (0,255,0),thick//6)
    cv2.imshow('teste',frame)
    if choice == 27:
        break
save.end_routine()
