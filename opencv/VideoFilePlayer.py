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

#  VideoFilePlayer.py

# encodig: utf-8

import sys
import os
import traceback
from time import sleep

sys.path.append('../')

from SOL4Py.ZApplication         import *
from SOL4Py.ZLabeledComboBox     import *
from SOL4Py.ZLabeledSlider       import *
from SOL4Py.ZApplicationView     import *
from SOL4Py.opencv.ZOpenCVImageView     import ZOpenCVImageView
from SOL4Py.opencv.ZOpenCVVideoCapture  import ZOpenCVVideoCapture

 
class MainView(ZApplicationView):
  
  # Constructor
  def __init__(self, title, x, y, width, height, device=0):
    super(MainView, self).__init__(title, x, y, width, height)
    self.video_capture = ZOpenCVVideoCapture()
    self.video_capture.open(device)
    self.image_view  = ZOpenCVImageView(self)
    self.add(self.image_view)
    title = str(device)
    self.set_filenamed_title(title)
    self.show()
  
  # Read a frame from a video buffer of the video capture, and set it the image view to draw it on the imag view     
  def render(self):
    if self.video_capture.is_opened():
      frame = self.video_capture.read()
      if frame.any() != None:
        self.image_view.set_opencv_image(frame)
        self.image_view.update()
        return True
    else:
      # If the video_capture closed, return False
      return False
 
  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.video_capture.close()
      self.video_capture.open(filename)
      self.set_filenamed_title(filename)
      

  def file_quit(self):
    self.terminated = True
    self.video_capture.close()
    self.close()
    

####
if main(__name__):
  try:
    name   = os.path.basename(sys.argv[0])
    applet = ZApplication(sys.argv)
        
    mainv  = MainView(name, 40, 40, 640,480, device="../../video/TokyoSkyTree.mp4")

    mainv.show ()
    
    applet.run(mainv)
    
  except:
    traceback.print_exc()

