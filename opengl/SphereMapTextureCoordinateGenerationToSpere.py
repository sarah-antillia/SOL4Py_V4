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

#  SphereMapTextureCoordinateGenerationToSphere.py

# See: http://cse.csusb.edu/tongyu/courses/cs520/notes/texture.php

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
from SOL4Py.opengl.ZOpenGLSolidSphere import *



class MainView(ZApplicationView):
  ##
  class OpenGLView(QGLWidget):

    def __init__(self, parent=None):
      super(QGLWidget, self).__init__(parent)


    def initializeGL(self):

      glShadeModel(GL_FLAT)
      glEnable(GL_DEPTH_TEST)
      glEnable(GL_CULL_FACE)

      self.filename = "./images/world.topo.bathy.200412.3x860x430.jpg"

      self.createTexture(self.filename)
      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
      glBindTexture(GL_TEXTURE_2D, 0)

        
    def createTexture(self, filename):

      self.id = glGenTextures(1);
      glBindTexture(GL_TEXTURE_2D, self.id)
      glPixelStorei(GL_UNPACK_ALIGNMENT, 4) 
      glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE);

      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
 
      #glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR);
      #glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR);
      
      glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP);
      glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP);

      self.image = ZOpenGLImage(filename, flip=False)
      w = self.image.width
      h = self.image.height
      
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)
      self.sphere = ZOpenGLSolidSphere(None, 1.5, 30, 30)
      
      
    def paintGL(self):
      glEnable(GL_DEPTH_TEST)     
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.2, 0.3)
      glLoadIdentity()
      gluLookAt(0.0, 2.0, 4.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

      glBindTexture(GL_TEXTURE_2D, self.id)
      glEnable(GL_CULL_FACE) 
      glCullFace(GL_BACK)

      glEnable(GL_TEXTURE_2D)
      
      glEnable(GL_TEXTURE_GEN_S);
      glEnable(GL_TEXTURE_GEN_T);
  
      glPushMatrix()
      self.sphere.draw()
      
      glPopMatrix()
      glDisable(GL_TEXTURE_GEN_S);
      glDisable(GL_TEXTURE_GEN_T);
  
      glDisable(GL_TEXTURE_2D)
      
      glBindTexture(GL_TEXTURE_2D, 0)
      glFlush()


    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      r = width/height
      glFrustum(-r, r, -1.0, 1.0, 2.0, 100.0);

      glMatrixMode(GL_MODELVIEW)
      

  ##
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
      
    self.show()


  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      
  def load_file(self, filename):
    self.opengl_view.createTexture(filename)    
    self.set_filenamed_title(filename)
      

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


