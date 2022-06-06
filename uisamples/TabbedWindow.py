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

#  TabbedWindow.py

# encodig: utf-8

import sys
import os
import traceback

from PyQt5.QtWidgets import *

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZTabbedWindow  import *
from SOL4Py.ZScrolledImageView import *

class MainView(ZApplicationView):
                
  def __init__(self, name, x, y, width, height):
    super(MainView, self).__init__(name, x, y, width, height, Z.Vertical)
  
    self.tabbed = ZTabbedWindow(self, 0, 0, width, height)

    name1 = "../images/ClassicCar.png"
    self.widget1 = ZScrolledImageView(self, 0, 0, width, height)
    self.widget1.load_image(name1)
    self.tabbed.add(name1, self.widget1)

    name2 = "../images/DecisionTree.png"
    self.widget2 = ZScrolledImageView(self, 0, 0, width, height)
    self.widget2.load_image(name2)
    self.tabbed.add(name2, self.widget2)

    name3 = "./TabbedWindow.py"
    self.widget3 = QTextEdit("Time to say goodbye") 
    read_text = open(name3, 'r').read()
    self.widget3.setText(read_text)
    self.tabbed.add(name3, self.widget3)

    self.add(self.tabbed)
    
if main(__name__):

  try:
    name = os.path.basename(sys.argv[0])

    applet = QApplication(sys.argv)
    
    main_view  = MainView(name, 40, 40, 800, 400) 
    main_view.show ()

    applet.exec_()

  except:
     traceback.print_exc()
     pass

