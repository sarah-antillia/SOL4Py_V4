# Copyright 2020-2021 antillia.com Toshiyuki Arai
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#  ZOpenCVVideoCapture.py
 
# 2018/05/05 Updated

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from SOL4Py.opencv.ZOpenCVImageConverter  import ZOpenCVImageConverter

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

class ZOpenCVVideoCapture:

  def __init__(self):
    self.target = 0
    self.video_capture   = cv2.VideoCapture()
    
  def open(self, target):
    self.target = target
    
    if isinstance(self.target, str):
      abspath = os.path.abspath(self.target)
      print("abspath:{}".format(abspath))
      if os.path.isfile(abspath):
        r = self.video_capture.open(abspath)
        if r == False:
          raise Error("Failed to open {}".format(abspath))
        else:
          print("Opened video_fille {}".format(abspath))
          return True
          
      else:
        raise FileNotFoundError(errno.ENOENT, 
              os.strerror(errno.ENOENT), abspath)
    elif isinstance(self.target, int):
      device_id = int(self.target)
     
      r = self.video_capture.open(device_id)
      if r == False:
        raise Error("Failed to open {}".format(device_id))
      else:
        print("Opened video_device {}".format(device_id))
        return True 
    else:
      return False
      
    
  def is_opened(self):
    return self.video_capture.isOpened()
    
  def close(self):
    self.video_capture.release()
    self.video_capture = None
    
  def set(self, prop_id, value):
    self.video_capture.set(prop_id, value)

  def get(self, prop_id):
    return self.video_capture.get(prop_id)
    
  def read(self):
    if self.is_opened():
      ret, frame = self.video_capture.read()
      if ret == True:
        return frame
      else:
        return None
        
    else:
      return None
  
  def close(self):
    if self.is_opened():
      self.video_capture.release()

