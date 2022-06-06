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

#  SolidSphere.py

# encodig: utf-8

import sys
import numpy as np

# 
sys.path.append('../')
from PIL import Image, ImageOps

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLLight import *
from SOL4Py.opengl.ZOpenGLMaterial import *
from SOL4Py.opengl.ZOpenGLGeometry import *

class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):

    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)

    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()
      gluLookAt(2.0, 4.0, 8.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

      glClearColor(0.0, 0.0, 0.0, 1.0)
      glEnable(GL_CULL_FACE) 
      glEnable(GL_LIGHTING)

      glEnable(GL_DEPTH_TEST)     
      light = ZOpenGLLight(GL_LIGHT0)
      light.position(10.0, 10.0, 10.0, 1.0)

      material = ZOpenGLMaterial(GL_FRONT)
      material.specular(1.0, 1.0, 1.0, 1.0) 
      material.shininess(100.0) 

      geometry = ZOpenGLGeometry(None)
      glPushMatrix()
      material.diffuse(0.0, 0.0, 1.0, 1.0)  
      glTranslate(-1.0, -2.0, -6.0)
      glRotate(-40.0, 1.0, 0.0, 0.0)
      geometry.solidSphere(3.0, 40, 40)
      glPopMatrix()


    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      r = width/height
      glFrustum(-r, r, -1.0, 1.0, 2.0, 100.0);

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
    glutInit(sys.argv)
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

