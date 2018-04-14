import time
import sys
import cv2
import os
import numpy as np
from datetime import datetime
from pytz import timezone
from .utilidades import get_timeNow
from .utilidades import createFolder
import csv
from time import time as timer
from .utilidades import Singleton
from .camera import camera_init

class saves(object,metaclass=Singleton):

    def __init__(self,demo,store,channel,resolution,MaxVideoTime):
        self.demo = demo
        self.store = store
        self.channel = channel
        self.resolution = resolution
        self.camera = camera_init(self.demo,self.store,self.channel,self.resolution)
        self.imagespath , self.videopath ,self.time = self.path_saves()
        self.videoWriter= self.video_partition()
        self.MaxVideoTime = MaxVideoTime
        self.csvwriter , self.file = self.csv_writter()

    def verify(self):
        if abs(self.time - timer()) > self.MaxVideoTime:
            self.imagespath , self.videopath ,self.time = self.path_saves()
            self.videoWriter= self.video_partition()
            self.time = timer()

    def save_video(self,frame):
        self.videoWriter.write(frame)

    def end_routine(self):
        self.videoWriter.release()
        self.camera.release()
        self.file.close()
        cv2.destroyAllWindows()

    def video_partition(self):
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            if self.demo == 0:#camera window
              fps = 1 / self._get_fps(frame)
              if fps < 1:
                    fps = 1
            else:
                    fps = round(self.camera.get(cv2.CAP_PROP_FPS))
            _, frame = self.camera.read()
            height, width, _ = frame.shape

            if self.demo == 'camera':
                    output_vid_file ='{}{}_camera{}_{}.avi'.format(self.videopath,self.store,self.channel,get_timeNow())
            else:
                    output_vid_file = '{}output_{}.avi'.format(self.videopath,os.path.basename(self.demo))

            print('Saving output video to {}...'.format(output_vid_file))
            videoWriter = cv2.VideoWriter(output_vid_file, fourcc, fps, (width, height))
            return videoWriter

    def cutBoudingBoxes(self,img,x, y, w, h,store,channel,person_id):
        cut=img[y:y+h,x:x+w]
        cv2.imwrite('{}ID{}_{}.jpg'.format(self.imagespath,person_id,get_timeNow()),cut)

    def csv_writter(self):
    # f = open('{}.csv'.format(file),'w')
        if self.demo == 'camera':
            output_csv_file ='output_{}_camera{}_{}.csv'.format(self.store,self.channel,get_timeNow())
        else:
            output_csv_file = 'output_{}.csv'.format( os.path.splitext( os.path.basename(self.demo) )[0] )
        print('Saving output video to {}...'.format(output_csv_file))
        f = open('{}{}'.format(self.videopath,output_csv_file),'w')
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['frame_id', 'track_id' , 'x', 'y', 'w', 'h','Confidence','TimeStamp'])
        f.flush()
        return writer,f

    def path_saves(self):
        if self.demo == 'camera':
            videopath ='./output/{}/camera{}/'.format(self.store,self.channel)
            imagespath ='./output/{}/camera{}/framecutted_{}/'.format(self.store,self.channel,get_timeNow())
        else:
            videopath ='./output/DataBase/'
            imagespath ='./output/DataBase/framecutted_{}/'.format(get_timeNow())
        time = timer()
        createFolder(imagespath)
        createFolder(videopath)
        return imagespath, videopath, time
