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

#  BufferedColoredRegularIcosahedron.py

# encodig: utf-8
import sys
import numpy as np
import math

from ctypes import *

sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *

from SOL4Py.opengl.ZOpenGLColoredRegularIcosahedron import *
from SOL4Py.openglarb.ZOpenGLBufferedShape import *


class MainView(ZOpenGLMainView):


  # Inner class starts.
  class OpenGLView(ZOpenGLView):
    ## Constructor
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)

    def initializeGL(self):

      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()

      glEnable( GL_DEPTH_TEST)
      glFrustum(1 , -1 , -1 , 1 , 1 , 10)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      vertexColors = [
        [ 1.0, 0.0, 0.0],
        [ 0.0, 1.0, 0.0], 
        [ 0.0, 0.0, 1.0], 
        [ 1.0, 1.0, 0.0],
        [ 0.0, 1.0, 1.0],
        [ 1.0, 0.0, 1.0],
        [ 1.0, 0.0, 0.0],
        [ 0.0, 1.0, 0.0], 
        [ 0.0, 0.0, 1.0], 
        [ 1.0, 1.0, 0.0],
        [ 0.0, 1.0, 1.0],
        [ 1.0, 0.0, 1.0],        
      ]
      self.hedron = ZOpenGLColoredRegularIcosahedron(vertexColors, len(vertexColors))
      
      self.shape  = ZOpenGLBufferedShape(self.hedron)

    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()
      glClearColor(0.0, 0.1, 0.2, 1.0)

      glPushMatrix()
      glTranslate(0.0,0.0,1.0)  
      gluLookAt(4.0, 12.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
      self.shape.draw()
      glPopMatrix()
 

    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)

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


