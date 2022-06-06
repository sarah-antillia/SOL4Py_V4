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

 
#  TorusWithColorEyeLightPositioner.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.ZColorPositioner import *
from SOL4Py.ZEyePositioner import *
from SOL4Py.ZLightPositioner import *
from SOL4Py.opengl.ZOpenGLLight import *
from SOL4Py.opengl.ZOpenGLMaterial import *
from SOL4Py.opengl.ZOpenGLQuadSurfaces import *
from SOL4Py.opengl.ZOpenGLGeometry import *


class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):

    def __init__(self, parent,  color, eye, light):
      #self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle = 0
      self.vcolor = color
      self.veye   = eye
      self.vlight = light
      

    def initializeGL(self):
      glEnable(GL_DEPTH_TEST)      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()                    
      glMatrixMode(GL_MODELVIEW)
    
      self.light    = ZOpenGLLight()
      self.material = ZOpenGLMaterial(GL_FRONT);
      self.geometry =  ZOpenGLGeometry(None)


    def paintGL(self):
      glFrustum(1 , -1 , -1 , 1 , 1 , 10);

      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glLoadIdentity();
      glMatrixMode(GL_MODELVIEW);
      glClearColor(1.0, 1.0, 1.0, 1.0);
      glTranslate(-0.5, -0.5, 0.0); 

      gluLookAt(self.veye[0], self.veye[1], self.veye[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0); 

      glRotate(0.0, 0.0, 1.0, 0.0);
      
      glEnable(GL_LIGHTING);
      self.light.position(self.vlight[0], self.vlight[1], self.vlight[2], 0.0);  

      self.material.diffuse(self.vcolor[0]/255.0, self.vcolor[1]/255.0, self.vcolor[2]/255.0, 0.0);
   
      self.material.specular(1.0, 1.0, 1.0, 0.0);
      self.material.shininess(100.0);
  
      glFrontFace(GL_CCW);

      glEnable(GL_CULL_FACE);
      glCullFace(GL_BACK);
      glEnable(GL_NORMALIZE);
        
      glPushMatrix();
      self.geometry.solidTorus(1.0, 1.8, 10, 50);
      glPopMatrix();

      glFlush();


    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width / height, 0.5, 40.0)

      glMatrixMode(GL_MODELVIEW);


    def setColorPosition(self, color):
      self.vcolor = color
      self.update()


    def setEyePosition(self, eye):
      self.veye = eye
      self.update()


    def setLigtPosition(self, light):
      self.vlight = light
      self.update()

  ##--------------------------------------------
  
  # class variables
  COLOR_RANGE = [0, 255]
  COLOR_POS   = [0.0, 0.0, 255.0]
  EYE_RANGE   = [-40, 40]
  EYE_POS     = [2.0, 8.0, 30.0]
  LIGHT_RANGE = [-40, 40]
  LIGHT_POS   = [0.0, 6.0, 2.0]
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)
    # 1 Create first imageview.

    self.opengl_view = self.OpenGLView(self, self.COLOR_POS, self.EYE_POS, self.LIGHT_POS)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)
    
    # 4 Add callbacks to positioners.
    self.colorPositioner.add_value_changed_callback(self.color_changed)
    self.eyePositioner.add_value_changed_callback  (self.eye_changed)
    self.lightPositioner.add_value_changed_callback(self.light_changed)

    self.show()


  # Add control pane to MainView
  def add_control_pane(self, fixed_width=270):
    self.vpane = ZVerticalPane(self, fixed_width)

    self.colorPositioner = ZColorPositioner(self, "ColorPositioner",["R", "G", "B"],
                               self.COLOR_RANGE, self.COLOR_POS)

    self.eyePositioner   = ZEyePositioner(self, "EyePositioner", ["X", "Y", "Z"],
                               self.EYE_RANGE, self.EYE_POS)
    
    self.lightPositioner = ZLightPositioner(self, "LightPositioner", ["X", "Y", "Z"],
                               self.LIGHT_RANGE, self.LIGHT_POS)

    self.vpane.add(self.colorPositioner)
    self.vpane.add(self.eyePositioner)
    self.vpane.add(self.lightPositioner)

    self.set_right_dock(self.vpane)


  def color_changed(self, v):
    values = self.colorPositioner.get_values()
    self.opengl_view.setColorPosition(values)


  def eye_changed(self, v):
    values = self.eyePositioner.get_values()
    self.opengl_view.setEyePosition(values)


  def light_changed(self, v):
    values = self.lightPositioner.get_values()
    self.opengl_view.setLigtPosition(values)


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

