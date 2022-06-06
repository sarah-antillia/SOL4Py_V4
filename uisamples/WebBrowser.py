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

#  WebBrowser.py
 
# 2018/05/01

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtCore import QUrl
from PyQtWebEngine import QWebEnginePage
from PyQtWebEngine import QWebEngineView

sys.path.append('../')

from SOL4Py.ZApplicationView import *



class WebBrowser(ZApplicationView):
  def __init__(self, title, x, y, width, height):
    super(WebBrowser, self).__init__(title, x, y, width, height, Z.Vertical)

    self.web_view = QWebEngineView(self)
    self.combobox = QComboBox(self)
    self.combobox.setEditable(True)
    self.combobox.activated[str].connect(self.combobox_activated)
    self.add(self.combobox)
    self.add(self.web_view)
    self.show()

  def load(self, url):
    self.combobox.addItem(url)
    self.web_view.load(QUrl(url))
   
  def combobox_activated(self, text):
    self.web_view.load(QUrl(text))
    

#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    web_browser = WebBrowser(app_name, 40, 40, 900, 380)
    web_browser.load("http://www.antillia.com") 
    web_browser.show ()

    applet.exec_()

  except:
     traceback.print_exc()
     pass

