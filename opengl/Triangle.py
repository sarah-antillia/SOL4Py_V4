﻿# Copyright 2020-2021 antillia.com Toshiyuki Arai
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

#  Triangle.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *

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
      glTranslatef(-1.5, 0.0, -6.0)

      glBegin(GL_QUADS)
      #Front
      self.redVertex  ( 0.0,  1.0, 0.0)
      self.greenVertex(-1.0, -1.0, 1.0)
      self.blueVertex ( 1.0, -1.0, 1.0)
 
      # Right
      self.redVertex  (0.0,  1.0,  0.0)
      self.blueVertex (1.0, -1.0,  1.0)
      self.greenVertex(1.0, -1.0, -1.0)
 
      # Back
      self.redVertex  ( 0.0,  1.0,  0.0)
      self.greenVertex( 1.0, -1.0, -1.0)
      self.blueVertex (-1.0, -1.0, -1.0)
 
      # Left
      self.redVertex  ( 0.0,  1.0,  0.0)
      self.blueVertex (-1.0, -1.0, -1.0)
      self.greenVertex(-1.0, -1.0,  1.0)
        
      glEnd()
      glFlush()

      
    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(50.0, width / height, 0.1, 50.0)

      glMatrixMode(GL_MODELVIEW)


    def redVertex(self, x, y, z):
      glColor3f(1.0, 0.0, 0.0)  
      glVertex3f(x, y, z)

    def greenVertex(self, x, y, z):
      glColor3f(0.0, 1.0, 0.0)  
      glVertex3f(x, y, z)

    def blueVertex(self, x, y, z):
      glColor3f(0.0, 0.0, 1.0)  
      glVertex3f(x, y, z)

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

