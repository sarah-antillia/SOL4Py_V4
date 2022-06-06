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

#  BufferedRegularIcosahedron.py

# encoding: utf-8

import sys
import os
import traceback

import traceback
import numpy as np
import math

sys.path.append('../')
from PIL import Image, ImageOps

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLRegularIcosahedron import *
from SOL4Py.openglarb.ZOpenGLBufferedShape import *


class MainView(ZOpenGLMainView):

  ## Inner class starts.
  class OpenGLView(ZOpenGLView):
    ## Constructor
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)


    def  initializeGL(self):
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()

      glEnable( GL_DEPTH_TEST)
      glFrustum(1 , -1 , -1 , 1 , 1 , 10)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      #//  gc -> loadIdentity()
    
      self.hedron = ZOpenGLRegularIcosahedron()
      
      self.shape = ZOpenGLBufferedShape(self.hedron)


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()
      glClearColor(0.0, 0.1, 0.2, 1.0)

      #Draw the first shape1.
      glPushMatrix()
      glTranslate(-2.0, 0.0, 1.0)  
      gluLookAt(0.0, 20.0, 30.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
      glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
      glColor(1.0, 1.0, 0.0)
      self.shape.draw()
      glPopMatrix()

      glPushMatrix()
      glTranslate(2.0, 0.0, 2.0)  
      gluLookAt(0.0, 20.0, 30.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
         
      glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
      glLineWidth(2.0)
      glColor(1.0, 0.0, 0.0)
      self.shape.draw()
        
      glPopMatrix()


    def resizeGL(self, w,  h):
      if w == 0 or h == 0:
        return
      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, w / h, 0.5, 40.0) 
      glMatrixMode(GL_MODELVIEW)

  ##--------------------------------------------


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)

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

    main_view = MainView(app_name, 40, 40, 640, 480)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()


