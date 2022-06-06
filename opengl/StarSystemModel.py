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

#  StarSystemModel.py

# encodig: utf-8

import sys
import os
import math
import traceback

from PyQt5.Qt import QMutex

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLTimerThread import *
from SOL4Py.opengl.ZOpenGLLight  import *
from SOL4Py.opengl.ZOpenGLMaterial  import *
from SOL4Py.opengl.ZOpenGLSolidSphere  import *
from SOL4Py.opengl.ZOpenGLCircle  import *

CIRCLE_ANGLE      = 360
INCREMENT         = [ 1.0, 0.7, 0.5, 0.2 ]
NUMBER_OF_PLANETS = 4

class MainView(ZOpenGLMainView):
  ##
  class OpenGLView(ZOpenGLView):
   
    def __init__(self, parent=None):
      super(ZOpenGLView, self).__init__(parent)
      self.parent = parent

      self.timerThread = None
      self.renderingInterval = 30
      self.mutex = QMutex()


    def initializeGL(self):
      self.angles = [0.0] * NUMBER_OF_PLANETS

      for i in range( NUMBER_OF_PLANETS):
        self.angles[i] = 30.0 * i

      self.sun     = None
      self.planets = [None] * NUMBER_OF_PLANETS
      self.orbits  = [None] * NUMBER_OF_PLANETS

      black         = [ 0.0, 0.0, 0.0, 1.0 ]
      ambient       = [ 0.5, 0.5, 0.5, 1.0 ]
      diffuse       = [ 0.2, 0.4, 0.8, 1.0 ]
      greendiffuse  = [ 0.0, 1.0, 0.0, 1.0 ]
      reddiffuse    = [ 1.0, 0.0, 0.0, 1.0 ]
      bluediffuse   = [ 0.0, 0.0, 1.0, 1.0 ]
      silverdiffuse = [ 0.8, 0.8, 0.8, 1.0 ]

      specular      = [ 1.0, 1.0, 1.0, 1.0 ]
      emission      = [ 0.8, 0.2, 0.0, 0.0 ]
      lowShining    = [ 10.0 ]
      highShining   = [100.0 ]
 
      sunMateria = ZOpenGLMateria(GL_FRONT, black,  diffuse, black, emission, highShining)
 
      self.sun = ZOpenGLSolidSphere(sunMateria, 0.5,  40, 40)

      self.orbits[0] = ZOpenGLCircle(0.0, 0.0, 0.0, 1.0)
      self.orbits[1] = ZOpenGLCircle(0.0, 0.0, 0.0, 1.6)
      self.orbits[2] = ZOpenGLCircle(0.0, 0.0, 0.0, 2.4)
      self.orbits[3] = ZOpenGLCircle(0.0, 0.0, 0.0, 2.9)

      materia    = [None] * NUMBER_OF_PLANETS

      materia[0] = ZOpenGLMateria(GL_FRONT, ambient, bluediffuse,   specular, black, lowShining)
      materia[1] = ZOpenGLMateria(GL_FRONT, ambient, silverdiffuse, specular, black, lowShining)
      materia[2] = ZOpenGLMateria(GL_FRONT, ambient, greendiffuse,  specular, black, lowShining)
      materia[3] = ZOpenGLMateria(GL_FRONT, ambient, reddiffuse,    specular, black, lowShining)
      
      self.planets[0] = ZOpenGLSolidSphere(materia[0], 0.10, 20, 20)
      self.planets[1] = ZOpenGLSolidSphere(materia[1], 0.18, 20, 20)
      self.planets[2] = ZOpenGLSolidSphere(materia[2], 0.18, 20, 20)
      self.planets[3] = ZOpenGLSolidSphere(materia[3], 0.12, 20, 20)
     
      self.timerThread = ZOpenGLTimerThread(self, self.renderingInterval)
      self.timerThread.start()


    def paintGL(self):
      self.mutex.lock()
      
      for i in range( NUMBER_OF_PLANETS):
        if (self.angles[i] < CIRCLE_ANGLE - INCREMENT[i]):
          self.angles[i] += INCREMENT[i]
        else:
          self.angles[i] = INCREMENT[i]

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

      glLoadIdentity()
      gluLookAt(-1.0, 8.0, 17.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

      glClearColor(0.0, 0.0, 0.0, 1.0)
      glEnable(GL_CULL_FACE) 
      glEnable(GL_LIGHTING)

      glColor(1.0, 1.0, 1.0) 

      glTranslate(0, 0, 0)
      self.sun.draw() # 0.0, 0.0, 0.0)
 
      light = ZOpenGLLight(GL_LIGHT0)
      lightPosition = [-2.0, 0.0, -1.0, 1.0]  
      light.positionv(lightPosition)

      for i in range(NUMBER_OF_PLANETS):
        pos = self.orbits[i].getOrbitPosition(int(self.angles[i]))
        glPushMatrix()
        glTranslate(pos[0], pos[1], pos[2])
        self.planets[i].draw()
        glPopMatrix()

      self.mutex.unlock()


    def resizeGL(self, w, h):
      if (w == 0 or h == 0) :
          return
      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, w / h, 0.5, 40.0) 

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

