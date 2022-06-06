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

#  MaterializedCubesRotationByKeyInput.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLMultiTexturedCube import *
from SOL4Py.opengl.ZOpenGLLight import *
from SOL4Py.opengl.ZOpenGLMaterial import *
from SOL4Py.opengl.ZOpenGLSolidCube import *
from SOL4Py.opengl.ZOpenGLWireCube import *

class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):
    CUBES = 4
    
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle = 0

    def initializeGL(self):
      glEnable(GL_DEPTH_TEST)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
      black         = [ 0.0, 0.0, 0.0, 1.0 ]
      ambient       = [ 0.5, 0.5, 0.5, 1.0 ]
      diffuse       = [ 0.2, 0.4, 0.8, 1.0 ]
      specular      = [ 1.0, 1.0, 1.0, 1.0 ]
      emission      = [ 0.8, 0.0, 0.0, 0.0 ]
      lowShining    = [ 10.0 ]
      highShining   = [100.0 ]

      mat1 = ZOpenGLMateria(GL_FRONT, ambient, diffuse, specular, emission, lowShining)
      mat2 = ZOpenGLMateria(GL_FRONT, black,   diffuse, specular, black,    lowShining)
      mat3 = ZOpenGLMateria(GL_FRONT, black,   diffuse, black,    emission, highShining)
      mat4 = ZOpenGLMateria(GL_FRONT, ambient, diffuse, specular, black,    highShining)
      self.materias = [mat1, mat2, mat3, mat4]
      self.cubes = []
      for i in range(self.CUBES):
        if i%2 ==0:
          self.cubes.append(ZOpenGLWireCube(self.materias[i], 0.5+0.2*i))
        else:
          self.cubes.append(ZOpenGLSolidCube(self.materias[i], 0.5+0.2*i) )
 
      self.light =   ZOpenGLLight(GL_LIGHT0)
      self.light.position(10.0, 10.0, 10.0, 1.0)


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glLoadIdentity()
      glTranslatef(0.0, 0.0, -1.0)
      gluLookAt(2.0, 6.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
      glEnable(GL_CULL_FACE) 
      glEnable(GL_LIGHTING)
      for i in range(self.CUBES):
        glPushMatrix()
        glRotate(self.angle, 0.0, 1.0, 0.0)
        glTranslate(-2.0+1.3*i, 0.5,  0.0+ 0.3*i)
        self.cubes[i].draw()
        glPopMatrix()

      glFlush()

      
    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)

      glMatrixMode(GL_MODELVIEW)


    def keyPressEvent(self, event):
      if event.key() == Qt.Key_Left:
        self.angle = self.angle - 2.0
      if event.key() == Qt.Key_Right:
        self.angle = self.angle + 2.0
      
      self.update()

  ##--------------------------------------------


  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
     
    self.show()


  def keyPressEvent(self, event):
    self.opengl_view.keyPressEvent(event)
    pass


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

