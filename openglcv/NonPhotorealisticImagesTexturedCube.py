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
 
#  NonPhotorealisticImagesTexturedCube.py

# encodig: utf-8

import sys
import os
import math
import traceback

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView      import *
from SOL4Py.opengl.ZOpenGLView          import *
from SOL4Py.opengl.ZOpenGLImage         import *
from SOL4Py.opengl.ZOpenGLMultiTexturedCube      import *
from SOL4Py.opencv.ZOpenCVImageInfo     import *
from SOL4Py.opencv.ZOpenCVImageReader   import *

class MainView(ZOpenGLMainView):
  ## Inner class
  class OpenGLView(ZOpenGLView):
    COUNT = 6   #The number of faces of a cube.

    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.faces      = [None] * self.COUNT
      self.imageInfos = [None] * self.COUNT
      self.cube       = None # OpenGLMultiTexturedCube
      self.angle      = 0


    def initializeGL(self):

      glEnable(GL_DEPTH_TEST);
      glEnable(GL_TEXTURE_2D);

      try:
        reader = ZOpenCVImageReader()
        originalImage = reader.read("../images/flower.png");

        self.faces[0] = cv2.stylization(originalImage); 
        _, self.faces[1] = cv2.pencilSketch(originalImage, sigma_s=10 , sigma_r=0.1, shade_factor=0.03); 
        self.faces[2] = cv2.edgePreservingFilter(originalImage, flags=cv2.RECURS_FILTER);    # RECURS_FILTER = Recursive Filtering 
        self.faces[3] = cv2.edgePreservingFilter(originalImage, flags=cv2.NORMCONV_FILTER);  # NORMCONV_FILTER = Normalized Convolution
        self.faces[4] = cv2.detailEnhance(originalImage);
        _, self.faces[5] = cv2.pencilSketch(originalImage,  sigma_s=60, sigma_r=0.07, shade_factor=0.03); 

        for i in range(self.COUNT):
          cvImageInfo = ZOpenCVImageInfo();
          self.imageInfos[i] = cvImageInfo.getImageInfo(self.faces[i], True);  
    
        self.cube = ZOpenGLMultiTexturedCube()
        self.cube.createTextureFromImageInfo(self.COUNT, self.imageInfos);

      except:
        traceback.print_exc()
        pass


    def paintGL(self):      
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.1, 0.1, 0.2, 1.0)
      glLoadIdentity()
     
      gluLookAt(2.0, 6.0, 11.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

      glTranslate(0.0, 0.0, 0.0);

      # Rotation around y-axis.
      glRotate(self.angle, 0.0, 1.0, 0.0);
      
      if self.cube != None:
        self.cube.draw()

      glFlush()

    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0);
      glMatrixMode(GL_MODELVIEW)
      glLoadIdentity()


    def keyPressEvent(self, event):
      if event.key() == Qt.Key_Left:
        self.angle = self.angle - 2.0
      if event.key() == Qt.Key_Right:
        self.angle = self.angle + 2.0
      
      self.update()



  ##
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
      
    self.show()


  def keyPressEvent(self, event):
    self.opengl_view.keyPressEvent(event)


#*************************************************
#    
if main(__name__):

  try:
    glutInit(sys.argv)
    
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 440)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()



