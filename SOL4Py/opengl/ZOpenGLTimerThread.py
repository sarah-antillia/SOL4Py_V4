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

#  ZOpenGLTimerThread.py

# encodig: utf-8

import sys
import os
import math
import traceback
import time
import threading

import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

 
class ZOpenGLTimerThread(QThread):

  # ZOpenGLTimerThread Constructor
  def __init__(self, opengl_view, interval = 200):  #200msec
    QThread.__init__(self)
    if opengl_view == None:
      raise ValueError("ZOpenGLTimerThread: opengl_view is None")
       
    self.opengl_view = opengl_view
    self.rendering_interval = interval/1000
    self.looping = True


  def terminate(self):
    self.looping = False


  def run(self):
    while self.looping == True:
      time.sleep(self.rendering_interval)
      self.opengl_view.update()

