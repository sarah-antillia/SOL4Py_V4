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

#  ScrolledImageView.py
 
# 2019/04/16 Updated to use ZApplicationView

# encodig: utf-8

import sys
import os
import traceback

import cv2
import errno

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *

sys.path.append('../')

from SOL4Py.ZApplicationView            import *
from SOL4Py.ZScrolledImageView  import ZScrolledImageView

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZImageView        import *
from SOL4Py.ZScaleComboBox    import *

class MainView(ZApplicationView):

  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height, Z.Vertical)
    self.image_view = ZScrolledImageView(self, 0, 0, width, height)
    filename = "../images/MeshedNioh.png"
    self.image_view.load_image(filename)
    self.add(self.image_view)
    self.set_filenamed_title(filename)
    
    self.show()


#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 500, 400)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()
    
