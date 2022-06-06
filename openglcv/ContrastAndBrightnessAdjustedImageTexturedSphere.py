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

#  ContrastAndBrightnessAdjustedTexturedSphere.py

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
#from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.opengl.ZOpenGLImageInfo import *
from SOL4Py.opencv.ZOpenCVImageInfo import *


class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):
    
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle = 120


    def initializeGL(self):
      glEnable(GL_DEPTH_TEST);
      glEnable(GL_TEXTURE_2D);

      self.light =   ZOpenGLLight(GL_LIGHT0)
      self.light.position(-10.0, -10.0, 20.0, 1.0)
      #self.light.position(10.0, 20.0, 0.0, 1.0)
      glFrontFace(GL_CCW);
      
      self.material = ZOpenGLMaterial(GL_BACK)
      white = [1.0, 1.0, 1.0, 1.0]
      blue  = [0.0, 0.0, 1.0, 1.0]
      shininess = 100
     
      self.material.diffusev(blue);
      self.material.specularv(white);
      self.material.shininess(shininess);
        
      self.sphere   = None
      self.axis = [-10.0, -10.0, 80.0]

      filename = "../opengl/images/world.topo.bathy.200412.3x860x430.jpg";

      self.createTexture(filename)
      self.parent.set_filenamed_title(filename)


    def createTexture(self, filename):
      try:
        reader = ZOpenCVImageReader();
        image = reader.read(filename);

        alpha = 12.0;
        beta  = 10.0; 
        convertedImage = cv2.convertTo(image, -1, alpha, beta);

        cvImageInfo = ZOpenCVImageInfo() ;
        
        #Get ZOpenGLImageInfo from cv2.Mat convertedImage
        
        imageInfo = cvImageInfo.getImageInfo(convertedImage);        
        
        self.sphere = ZOpenGLTexturedSphere(2.5, 40, 40);
        self.sphere.imageFromImageInfo(1, imageInfo)
        
      except:
        traceback.print_exc()


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
      glClearColor(0.0, 0.0, 0.0, 0.0)
      glLoadIdentity()
      glTranslatef(0.0, 0.0, -1.0)
      gluLookAt(0.0, -5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);

      glEnable(GL_CULL_FACE) 
      glEnable(GL_LIGHTING)

      glTranslatef(0.0, 0.0, 0.0)
      glRotate(self.angle, self.axis[0], self.axis[1], self.axis[2]);
      if self.sphere != None:
        self.sphere.draw()

      glFlush()


    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width/height, 0.5, 100)
      glMatrixMode(GL_MODELVIEW)


    def keyPressEvent(self, event):
      if event.key() == Qt.Key_Left:
        self.angle = self.angle - 2.0
      if event.key() == Qt.Key_Right:
        self.angle = self.angle + 2.0
      
      self.update()


    def createTexture(self, filename):
      self.sphere = ZOpenGLTexturedSphere(filename, None, 1.0, 40, 40);

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
  
    main_view = MainView(app_name, 40, 40, 500, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

