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
 
#  Fog.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
#from SOL4Py.opengl.ZOpenGLQuadric import *
#from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.opengl.ZOpenGLFog import *


class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):

    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)


    def initializeGL(self):
      glEnable(GL_DEPTH_TEST)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
      self.fog = ZOpenGLFog()
      glFrustum(1 , -1 , -1 , 1 , 1 , 10);


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)

      glLoadIdentity()

      glMatrixMode(GL_PROJECTION);
      
      glFrustum(1 , -1 , -1 , 1 , 1 , 10);
  
      self.fog.enable()

      self.fog.mode(GL_LINEAR);
      self.fog.color(0.0, 0.0, 1.0, 0.0);
      self.fog.start(1.0);
      self.fog.end(10.0);
      
      glBegin(GL_POLYGON);
      vertices = [
        [ 0.0, -0.9 , -2.0],
        [ 3.0, -0.9 , -7.0],
        [ 0.0,  0.9 , -2.0],
        [ 0.0, -0.9 , -2.0],
        [-3.0, -0.9 , -7.0],
        [ 0.0 , 0.9 , -2.0]
      ]
      self.draw(vertices)
      glEnd();
      self.fog.disable()

      glFlush()


    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)
      #glFrustum(1 , -1 , -1 , 1 , 1 , 10);

      glMatrixMode(GL_MODELVIEW)


    def draw(self, vertices_list):
      for i in range(len(vertices_list)):
        v = vertices_list[i]
        glVertex3f(v[0], v[1], v[2])
  
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

