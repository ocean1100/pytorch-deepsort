import time
import sys
import cv2
import os
import numpy as np
import hashlib
import pprint
import json
import requests
from itertools import chain
from datetime import datetime, date
from pytz import timezone
from datetime import datetime
from pytz import timezone

pp = pprint.PrettyPrinter(indent = 4)

class Singleton(type):
   _instances = {}
   def __call__(cls, *args, **kwargs):
       if cls not in cls._instances:
           cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
       return cls._instances[cls]

def process_box(self, b, h, w, threshold):
        max_indx = np.argmax(b.probs)
        max_prob = b.probs[max_indx]
        label = self.meta['labels'][max_indx]
        if max_prob > threshold:
                left  = int ((b.x - b.w/2.) * w)
                right = int ((b.x + b.w/2.) * w)
                top   = int ((b.y - b.h/2.) * h)
                bot   = int ((b.y + b.h/2.) * h)
                if left  < 0    :  left = 0
                if right > w - 1: right = w - 1
                if top   < 0    :   top = 0
                if bot   > h - 1:   bot = h - 1
                mess = '{}'.format(label)
                return (left, right, top, bot, mess, max_indx, max_prob)
        return None

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def asList(data):
    return list(chain.from_iterable(data))

def get_timeNow_str():
    return str(get_timeNow())

def get_timeNow():
    return datetime.now(timezone('Brazil/East'))
def get_weekday():
    return datetime.date(get_timeNow()).weekday()

def get_timestring_to_mili(timeString):
    hora, minuto, segundo = timeString.split('.')[3:-1]
    now = datetime.now()
    now.replace(hour = int(hora))
    now.replace(minute = int(minuto))
    now.replace(second = int(segundo))
    return now
def limpaLista(lista):
    res = []
    for i in lista:
        if not i in res:
            res.append(i)
    return res
