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

#  ScrolledImageViewer.py

# encodig: utf-8

import sys
import os
import cv2
import traceback


# 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZVerticalPane    import ZVerticalPane 
from SOL4Py.opencv.ZOpenCVScrolledImageView    import *
from SOL4Py.opengl.ZOpenGLView    import *
from SOL4Py.opengl.ZOpenGLTexture2D    import *
from SOL4Py.opengl.ZOpenGLImageInfo import *
from SOL4Py.opencv.ZOpenCVImageReader import *
from SOL4Py.opencv.ZOpenCVImageInfo import *

 
class MainView(ZApplicationView):
  
  class OpenCVView(ZOpenCVScrolledImageView):
    def __init__(self, parent, x, y, width, height):
      ZOpenCVScrolledImageView.__init__(self, parent)
      filename = "../images/Figure.png"
      #filename = "../images/ClassicCar.png"; 
      self.load_opencv_image(filename)
      self.setGeometry(x, y, width, height)
      self.update()
      
  
  class OpenGLView(ZOpenGLView):
    
    def __init__(self, parent, x, y, width, height):
      super(ZOpenGLView, self).__init__(parent)
      self.parent = parent

      self.angle = 120
      self.texture  = None
      self.setGeometry(x, y, width, height)


    def initializeGL(self):
      glEnable(GL_DEPTH_TEST);
      glEnable(GL_TEXTURE_2D);

      self.texture = ZOpenGLTexture2D();
      reader = ZOpenCVImageReader();
      #filename = "../images/ClassicCar.png"; 
      filename = "../images/Figure.png"; 
      
      image = reader.read(filename);
      self.sharpend = self.sharpen(image);
      self.texture.bind();
      
      self.imageToTexture(self.sharpend)

      self.texture.parameter(GL_TEXTURE_MIN_FILTER, GL_LINEAR);
      self.texture.parameter(GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      self.texture.env(GL_TEXTURE_ENV_MODE, GL_MODULATE); 

      self.texture.unbind()


    def sharpen(self, image):  # originalImage = cv2.Mat  
      ksize  = 21
      sigma  = 12
    
      blurred = cv2.GaussianBlur(image, (ksize, ksize), 
            float(sigma), #sigmaX, 
            float(sigma), #sigmaY
            cv2.BORDER_DEFAULT)

      alpha = 2.5
      beta  = 1.0 - alpha
      return cv2.addWeighted(image, alpha, blurred, beta, 0.0)
      

    def imageToTexture(self, image):
      cvImageInfo = ZOpenCVImageInfo()
      imageInfo   =   cvImageInfo.getImageInfo(image);
      self.texture.imageFromImageInfo(imageInfo);


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glClearColor(1.0, 1.0, 1.0, 1.0);
          
      glMatrixMode(GL_MODELVIEW);
      glLoadIdentity();
      gluLookAt(2.0, 4.0, 6.0, 0., 0., 0., 0., 1., 0.);

      self.texture.bind()
      glBegin(GL_QUADS);

      glTexCoord2f(0.0, 0.0)
      glVertex(-1.0,  1.0, 0.0);

      glTexCoord2f(1.0, 0.0)
      glVertex( 1.0,  1.0, 0.0);

      glTexCoord2f(1.0, 1.0)
      glVertex( 1.0, -1.0, 0.0);

      glTexCoord2f(0.0, 1.0)
      glVertex(-1.0, -1.0, 0.0);

      glEnd();
      self.texture.bind()
      glFlush()


    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width/height, 0.5, 100)
      glMatrixMode(GL_MODELVIEW)
    
    
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    
    # 1 Create the first imageview.
    self.image_views = [None, None]
    self.image_views[0] = self.OpenCVView(self, 0, 0, width/2, height)

    # 2 Create the second imageview.
    self.image_views[1] = self.OpenGLView(self, 0, 0, width/2, height)

    # 2 Add the image view to a main_layout of this main view.
    for i in range (len(self.image_views)):
       self.add(self.image_views[i])
      
    self.show()
  
      

#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 460)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


