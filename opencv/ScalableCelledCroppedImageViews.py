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

#  ScalableCelledCroppedImageViews.py

# 2019/04/17


# encodig: utf-8

import sys
import os
import traceback
import errno
import cv2

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZImageView        import *
from SOL4Py.ZScaleComboBox    import *
from SOL4Py.ZVerticalPane    import *
from SOL4Py.ZLabeledComboBox  import *
from SOL4Py.opencv.ZOpenCVCroppedImageReader import *


class MainView(ZApplicationView):

  IMAGE_COUNT = 9
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height, Z.Vertical)

    self.get_layout().setSpacing(0)
    self.get_layout().setContentsMargins(0,0,0,0);
   
    self.scale_combobox = ZScaleComboBox(self.main_layouter, "Scale")
    self.scale_combobox.set_current_scale("80%")
    
    self.add(self.scale_combobox)
    
    self.image_views = [None] * self.IMAGE_COUNT
    
    filenames   = ["../images/flower1.jpg", "../images/flower2.jpg", "../images/flower.png", 
                   "../images/Redleaves.jpg", "../images/flower5.jpg", "../images/flower6.jpg", 
                   "../images/flower7.jpg", "../images/flower8.png", "../images/flower9.png", 
                   ]
    
    # 1 Create an inner widget.
    self.inner = QWidget(self.main_layouter)
    
    # 2 Set QSizePolicy.Expanding to the self.inner
    self.inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    # 3 Create a grid layout for the self.inner.
    self.grid  = QGridLayout(self.inner)

    # 4 Add instances of ZImageView to the self.grid.
    
    try:
 
      for i in range(self.IMAGE_COUNT):  
        self.image_views[i] = ZImageView(self, 0, 0, 300, 300)
        image = self.load_cropped_scaled_image(filenames[i], (224, 224)) #VGG16 input size
        self.image_views[i].set_image(image)
        self.image_views[i].rescale(80)
        x = int(i % 3)
        y = int(i / 3)
        self.grid.addWidget(self.image_views[i], y, x)

    except:
      traceback.print_exc()

    # 5 Add the self.inner to the self.
    self.add(self.inner)

    # 6 Add the scaled_changed callback to the self.scale_combobox.
    self.scale_combobox.add_activate_callback(self.scale_changed)
    
    self.show()


  def load_cropped_scaled_image(self, filename, scale):
    reader  = ZOpenCVCroppedImageReader()
    image   = reader.read(filename)
    cropped = reader.crop_max_square_region(image)
    scaled  = cv2.resize(cropped, dsize=scale)
    return scaled


  # Scale changed callback
  def scale_changed(self, text):
    text = text.replace("%", "")
    scale = int(text)
    
    # Hide self.inner to avoid the flickering caused by rescaling of image_views.
    self.inner.hide()

    for i in range(self.IMAGE_COUNT):
      self.image_views[i].rescale(scale)
    
    # You should call update method of self.grid layout
    self.grid.update()

    # Show self.inner.   
    self.inner.show()
 


#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 640, 640)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

