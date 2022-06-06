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

#  We have used 'world.topo.bathy.200412.3x5400x2700.jpg' file in the following page.
# 
# http:# visibleearth.nasa.gov/view.php?id=73909
# 
# December, Blue Marble Next Generation w/ Topography and Bathymetry
# Credit: Reto St?ckli, NASA Earth Observatory

#  We have also used the following Mars map:
#  Owner: Caltech/JPL/USGS 
# https:# maps.jpl.nasa.gov/pix/mar0kuu2.jpg

#  TexturedSpheresWithAxisEyeAndLightPositioner.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLLight import *
from SOL4Py.opengl.ZOpenGLMaterial import *
from SOL4Py.opengl.ZOpenGLTexturedSphere import *
from SOL4Py.opengl.ZOpenGLSphere import *
from SOL4Py.opengl.ZOpenGLQuadric import *
from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.ZLabeledSlider import *
from SOL4Py.ZEyePositioner import *
from SOL4Py.ZLightPositioner import *


class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):
    
    def __init__(self, parent, angle, axis, eye, light):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle  = angle
      self.axis   = axis
      self.veye   = eye
      self.vlight = light

    def initializeGL(self):
      #glShadeModel(GL_FLAT)
      #glEnable(GL_DEPTH_TEST)      
      #glMatrixMode(GL_PROJECTION)
      #glLoadIdentity()                    
      #glMatrixMode(GL_MODELVIEW)

      self.light =   ZOpenGLLight(GL_LIGHT0)
      
      #self.material = ZOpenGLMaterial(GL_FRONT)
      self.sphere   = None
      
      filename = "./images/ven0aaa2.jpg";

      self.createTexture(filename)
      self.parent.set_filenamed_title(filename)
  

    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glLoadIdentity()

      #gluLookAt(0.0, 2.0, -1.0, 0.0, 0.0, 0.0, 0.0, 30.0, 0.0);
      gluLookAt(self.veye[0], self.veye[1], self.veye[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0); 

      glEnable(GL_LIGHTING)
      self.light.position(self.vlight[0], self.vlight[1], self.vlight[2], 0.0);  

      glTranslatef(0.0, 0.0, 0.0)
      glRotate(self.angle, self.axis[0], self.axis[1], self.axis[2]);
      #self.material.diffuse(0.0, 0.0, 1.0, 1.0);
   
      #self.material.specular(1.0, 1.0, 1.0, 0.0);
      #self.material.shininess(100.0);
 
      if self.sphere != None:
        self.sphere.draw()


    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      glFrustum(width / height, -width / height, -1.0, 1.0, 2.0, 30.0);
      glMatrixMode(GL_MODELVIEW)


    def createTexture(self, filename):
      self.sphere = ZOpenGLTexturedSphere(filename, None, 1.0, 40, 40);

    def setAngle(self, angle):
      self.angle = angle
      self.update()


    def setAxisPosition(self, axis):
      self.vaxis = axis
      self.update()


    def setEyePosition(self, eye):
      self.veye = eye
      self.update()


    def setLigtPosition(self, light):
      self.vlight = light
      self.update()

  ##--------------------------------------------
  # class variables
  MIN_ANGLE   = -180
  MAX_ANGLE   = 180
  CUR_ANGLE   = 128
  AXIS_RANGE  = [-100, 100]
  AXIS_POS    = [-10,  -50, 80.0]
  EYE_RANGE   = [-200, 200]
  EYE_POS     = [0.0, 1.0, 2]
  LIGHT_RANGE = [-200, 200]
  LIGHT_POS   = [-14.0, -10, -70.0]

  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)

    # 1 Create first imageview.
    self.opengl_view = self.OpenGLView(self, self.CUR_ANGLE, 
                          self.AXIS_POS, self.EYE_POS, self.LIGHT_POS)

    # 2 Add the image view to a main_layout of this main view.
    self.add(self.opengl_view)

    # 3 Add callbacks to positioners.
    self.rotator.add_value_changed_callback(self.angle_changed)
    self.axisPositioner.add_value_changed_callback(self.axis_changed)
    self.eyePositioner.add_value_changed_callback  (self.eye_changed)
    self.lightPositioner.add_value_changed_callback(self.light_changed)

    self.show()

  # Add control pane to MainView
  def add_control_pane(self, fixed_width=270):
    self.vpane = ZVerticalPane(self, fixed_width)

    self.rotator       = ZLabeledSlider(self, "Rotator", False,
                               self.MIN_ANGLE, self.MAX_ANGLE, self.CUR_ANGLE) 

    self.axisPositioner = ZPositioner(self, "AXISPositioner",["X", "Y", "Z"],
                               self.AXIS_RANGE, self.AXIS_POS)

    self.eyePositioner   = ZEyePositioner(self, "EyePositioner", ["X", "Y", "Z"],
                               self.EYE_RANGE, self.EYE_POS)
    
    self.lightPositioner = ZLightPositioner(self, "LightPositioner", ["X", "Y", "Z"],
                               self.LIGHT_RANGE, self.LIGHT_POS)

    self.vpane.add(self.rotator)
    self.vpane.add(self.axisPositioner)
    
    self.vpane.add(self.eyePositioner)
    self.vpane.add(self.lightPositioner)

    self.set_right_dock(self.vpane)


  def angle_changed(self, value):
    self.rotator.set_value_text(str(value))
    self.opengl_view.setAngle(value)


  def axis_changed(self, v):
    values = self.axisPositioner.get_values()
    self.opengl_view.setAxisPosition(values)


  def eye_changed(self, v):
    values = self.eyePositioner.get_values()
    self.opengl_view.setEyePosition(values)


  def light_changed(self, v):
    values = self.lightPositioner.get_values()
    self.opengl_view.setLigtPosition(values)


  # Show FileOpenDialog and select an image file.
  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)


  def load_file(self, filename):
    self.opengl_view.createTexture(filename)    
    self.set_filenamed_title(filename)


#*************************************************
#    
if main(__name__):

  try:
    glutInit(sys.argv)
    
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 840, 490)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

