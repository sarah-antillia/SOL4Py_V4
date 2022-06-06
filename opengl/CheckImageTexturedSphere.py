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

#  CheckImageTexturedCube.py

# encodig: utf-8

import sys
import numpy as np
import math

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLTexturedSphere import *
from SOL4Py.opengl.ZCheckImage import *

class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class CheckImageTexturedSphere(ZOpenGLTexturedSphere):

    def __init__(self):
      ZOpenGLTexturedSphere.__init__(self, None, None, 1.0, 100, 100)
      check_image = ZCheckImage()
       
      self.bind()

      self.pixelStore(GL_UNPACK_ALIGNMENT, 1)
      self.parameter(GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
      self.parameter(GL_TEXTURE_MIN_FILTER, GL_NEAREST) 

      self.env(GL_TEXTURE_ENV_MODE, GL_MODULATE)

      self.parameter(GL_TEXTURE_WRAP_S, GL_REPEAT)
      self.parameter(GL_TEXTURE_WRAP_T, GL_REPEAT)

      self.image(0, GL_RGBA, check_image.WIDTH, check_image.HEIGHT, 
                    0, GL_RGBA, GL_UNSIGNED_BYTE, check_image.data )
      self.unbind()

  ##
  class OpenGLView(ZOpenGLView):

    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)


    def initializeGL(self):
      glEnable(GL_DEPTH_TEST)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
      
      self.texture = MainView.CheckImageTexturedSphere()


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glColor(1.0, 1.0, 1.0)
      glLoadIdentity()
      glTranslatef(0.0, 0.0, 0.0)
      gluLookAt(2.0, 6.0, 10.0, 0.0, 0.0, 0.0, 0.0, 10.0, 0.0) 
      #glEnable(GL_CULL_FACE);  
      #glCullFace(GL_BACK);
      glRotate(10.0, 1.0, 0.0, 0.0)
      
      self.texture.draw()
      
      glFlush()


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
    glutInit(sys.argv)
    
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

