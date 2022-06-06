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

#  ColoredPyramid.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLObject import *

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

    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glLoadIdentity()
      glTranslate(0.0, 0.0, -1.0) 
      gluLookAt(2.0, 4.0, 6.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
      glEnableClientState(GL_VERTEX_ARRAY) 
      glEnableClientState(GL_COLOR_ARRAY)

      vertices = [
        -0.5, -0.5, -0.5, 
         0.5, -0.5, -0.5, 
         0.5, -0.5,  0.5, 
        -0.5, -0.5,  0.5, 
         0.0,  0.5,  0.0, 
        ]
    
      #Colors(RGBAs) for the 5 vertices
      colors = [ 
        0.0, 0.0, 1.0, 1.0, 
        0.0, 1.0, 0.0, 1.0, 
        0.0, 0.0, 1.0, 1.0, 
        0.0, 1.0, 0.0, 1.0, 
        1.0, 0.0, 0.0, 1.0  
      ]
  
      #Indices for the 4 triangles.
      indices = [ 
        2, 4, 3,   
        1, 4, 2,   
        0, 4, 1,   
        4, 0, 3    
      ]
      avertices =  np.array(vertices, dtype="float32")
      acolors   =  np.array(colors, dtype="float32")
      
      glVertexPointer(3, GL_FLOAT, 0, avertices)
      glColorPointer (4, GL_FLOAT, 0, acolors)
      nindices     =  np.array(indices, dtype="uint32")

      glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, nindices)
      glDisableClientState(GL_VERTEX_ARRAY) 
      glDisableClientState(GL_COLOR_ARRAY)

      glFlush()

    def draw(self, vertices_list):
      for i in range(len(vertices_list)):
        v = vertices_list[i]
        glVertex3f(v[0], v[1], v[2])
 
 
    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)

      glMatrixMode(GL_MODELVIEW)


  ##Inner class ends
  
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
  
    main_view = MainView(app_name, 40, 40, 600, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

