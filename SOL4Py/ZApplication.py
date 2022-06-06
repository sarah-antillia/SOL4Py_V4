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

#  ZApplication.py

# encodig: utf-8

import sys
import os
import traceback
from time import sleep

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SOL4Py.ZApplicationView import *

#---------------------------------------------------------------------

class ZApplication(QApplication):
  
  def __init__(self, argv):
    super(ZApplication, self).__init__(argv)
   
  
  def run(self, view, interval= 0.001):
    # Check sleep interval
    if interval < 0.0001 or interval >1.0:
      interval = 0.001
      
    if isinstance(view, ZApplicationView):
      while True:
        QApplication.processEvents()
        sleep(interval)      
        view.render()
        if view.is_terminated():
          break
    else:
      print("Invalid view parameter")    

  def exec(self, interval= 0.001):
    # Check sleep interval
    if interval < 0.0001 or interval >1.0:
      interval = 0.001
      
    while True:
        QApplication.processEvents()
        sleep(interval)      
       # if view.is_terminated():
       #   break


def main(name):    
  if name == '__main__':
    return True
  else:
    return False

      
