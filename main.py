# run.py ---
#
# Filename: run.py
# Description:
# Author: https://github.com/bendidi
# Maintainer: Sergio-Feliciano Mendoza-Barrera
# Created: Fri Mar  9 12:09:44 2018 (-0600)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 7
# URL:
# Doc URL:
# Keywords:
# Compatibility:
#
#

# Commentary:
#
#
#
#

# Change Log:
#
#
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU

# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
#
#

# Code:
from darkflow.darkflow.defaults import argHandler #Import the default arguments
import os
from darkflow.darkflow.net.build import TFNet


FLAGS = argHandler()
FLAGS.setDefaults()

#FLAGS.demo = "/home/guilhermemercurio/Python/DataBase/CameraEasyNDisplay.mp4"

FLAGS.demo = "camera" #Real time camera using RSTP protocol, channel 3 low resolution
FLAGS.store="newera"
FLAGS.channel = 2 #Number of the camera in New Era, 1 to 8
FLAGS.resolution = 2 # Two options 1: High resolution 2:Low resolution
FLAGS.neptune = False

FLAGS.model = "darkflow/cfg/yolo.cfg" # tensorflow model
FLAGS.load = "darkflow/bin/yolo.weights" # tensorflow weights
# FLAGS.pbLoad = "tiny-yolo-voc-traffic.pb" # tensorflow model
# FLAGS.metaLoad = "tiny-yolo-voc-traffic.meta" # tensorflow weights
FLAGS.threshold = 0.3 # threshold of decetion confidance (detection if confidance > threshold )
FLAGS.gpu = 0.60 #how much of the GPU to use (between 0 and 1) 0 means use cpu
FLAGS.track = True # wheither to activate tracking or not
# FLAGS.trackObj = ['Bicyclist','Pedestrian','Skateboarder','Cart','Car','Bus'] # the object to be tracked
FLAGS.trackObj = ["person"]
FLAGS.BK_MOG = False # activate background substraction using cv2 MOG substraction,
                    # to help in worst case scenarion when YOLO cannor predict(able to detect mouvement, it's not ideal but well)
                    # helps only when number of detection < 3, as it is still better than no detection.
# FLAGS.tracker = "sort" # wich algorithm to use for tracking deep_sort/sort (NOTE : deep_sort only trained for people detection )
FLAGS.tracker = "deep_sort"

FLAGS.skip = 0 # how many frames to skipp between each detection to speed up the network
FLAGS.csv = True #whether to write csv file or not(only when tracking is set to True)
FLAGS.saveVideo = True  #whether to save the video or not
FLAGS.display = True # display the tracking or not

tfnet = TFNet(FLAGS)

tfnet.camera()
exit('Demo stopped, exit.')

#
# run.py ends here
