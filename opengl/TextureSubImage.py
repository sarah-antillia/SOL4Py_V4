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
 
#  TextureSubImage.py

# encodig: utf-8

import sys
import os
import math
import traceback

import numpy as np

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtOpenGL     import *

import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image, ImageOps

# 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZScalableScrolledImageView  import *
from SOL4Py.ZVerticalPane    import * 
from SOL4Py.opengl.ZOpenGLImage     import *

class MainView(ZApplicationView):
  ##
  class OpenGLView(QGLWidget):

    def __init__(self, parent=None):
      super(QGLWidget, self).__init__(parent)


    def initializeGL(self):
      glShadeModel(GL_FLAT)
      glEnable(GL_DEPTH_TEST)
      glEnable(GL_CULL_FACE)

      self.createTexture("../images/Flower.png");
      self.setSubImage("../images/Nanten.png", 0, 20, 20);
      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
      glBindTexture(GL_TEXTURE_2D, 0)


    def createTexture(self, filename):
      self.id = glGenTextures(1);
      glBindTexture(GL_TEXTURE_2D, self.id)
      glPixelStorei(GL_UNPACK_ALIGNMENT,1) 

      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP)
      glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP)
 
      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL )
 
      self.image = ZOpenGLImage(filename)
      w = self.image.width
      h = self.image.height
      
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)


    def setSubImage(self, filename, level, xoffset, yoffset):
      self.subimage = ZOpenGLImage(filename)
      w = self.subimage.width
      h = self.subimage.height

      glTexSubImage2D(GL_TEXTURE_2D,
        level,  
        xoffset,  
        yoffset,  
        w,  
        h,  
        GL_RGBA,  
        GL_UNSIGNED_BYTE,  
        self.subimage.bytes); 


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.2, 0.3)
      glLoadIdentity()

      glBindTexture(GL_TEXTURE_2D, self.id)
      
      glEnable(GL_TEXTURE_2D)

      glPushMatrix()

      glBegin(GL_QUADS)
      glTexCoord2d(0.0, 1.0)
      glVertex3d(-1.0, -1.0,  0.0)
      glTexCoord2d(1.0, 1.0)
      glVertex3d( 1.0, -1.0,  0.0)
      glTexCoord2d(1.0, 0.0)
      glVertex3d( 1.0,  1.0,  0.0)
      glTexCoord2d(0.0, 0.0)
      glVertex3d(-1.0,  1.0,  0.0)
      glEnd()

      glPopMatrix()

      glDisable(GL_TEXTURE_2D)
      glFlush()



    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return;
       
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      #glFrustum(-r, r, -1.0, 1.0, 2.0, 100.0)

      glMatrixMode(GL_MODELVIEW);
      glLoadIdentity()

  ##
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
      
    self.show()


#*************************************************
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 440)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()




