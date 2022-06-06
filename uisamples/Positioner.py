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

#  Positioner.py

# encodig: utf-8

import sys
import os
import traceback

from PyQt5.QtWidgets import *

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZImageView    import *
from SOL4Py.ZPositioner import *

class MainView(ZApplicationView):
  # Inner classes
  #--------------------------------------------
  class SourceImageView(ZImageView):
    def __init__(self, parent, x, y, width, height):
      ZImageView.__init__(self, parent, x, y, width, height)

    def load(self, filename):
      self.load_image(filename)
      self.update()
   
      
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    
    # 1 Create first imageview.
    self.source_image_view = self.SourceImageView(self, 0, 0, width/2, height/2) 

    filename = "../images/NiohLiken.png"

    # 3 Load the file
    self.load_file(filename)
         
    # 4 Add imageviews to the main_layout which is a horizontal layouter.
    self.add(self.source_image_view)

    self.show()
  

  def add_control_pane(self, fixed_width=300):
    # Control pane widget
    print("add_control_pane")
    self.vpane = ZVerticalPane(self, fixed_width)
    self.positioner = ZPositioner(self)
    self.positioner.add_value_changed_callback(self.slider_value_changed)
  
    self.vpane.add(self.positioner)
    
    self.set_right_dock(self.vpane)    

   
  def load_file(self, filename):
    self.source_image_view.load(filename)
    self.set_filenamed_title(filename)
 
  def slider_value_changed(self, value):
    print("slider value changed:{}".format(value))
    
    values = self.positioner.get_values()
    print(values[0])
    print(values[1])
    print(values[2])

     
#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

