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

#  DenoisedImageTexture.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLTexture2D import *
from SOL4Py.opengl.ZOpenGLImageInfo import *
from SOL4Py.opencv.ZOpenCVImageReader import *
from SOL4Py.opencv.ZOpenCVImageInfo import *


class MainView(ZOpenGLMainView):
  ##--------------------------------------------
  class OpenGLView(ZOpenGLView):
    
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)
      self.angle = 120
      self.textured = False
      self.texture  = None
      self.denoisedImage = None


    def initializeGL(self):
      glEnable(GL_DEPTH_TEST);
      glEnable(GL_TEXTURE_2D);

      self.texture = ZOpenGLTexture2D();
      reader = ZOpenCVImageReader();
      filename = "../images/MeshedNioh.png"; 
      
      image = reader.read(filename);
      self.denoised = self.denoise(image);
      self.texture.bind();
      
      self.imageToTexture(self.denoised)
      

      self.texture.parameter(GL_TEXTURE_MIN_FILTER, GL_LINEAR);
      self.texture.parameter(GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      self.texture.env(GL_TEXTURE_ENV_MODE, GL_MODULATE); 

      self.texture.unbind()


    def denoise(self, image):  # originalImage = cv2.Mat      
      hParameter         = 27.0;
      templateWindowSize = 15;
      searchWindowSize   = 13;

      return cv2.fastNlMeansDenoising(image, hParameter, 
             templateWindowSize, searchWindowSize);


    def imageToTexture(self, image):
      cvImageInfo = ZOpenCVImageInfo()
      imageInfo   =   cvImageInfo.getImageInfo(image);
      self.texture.imageFromImageInfo(imageInfo);


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glClearColor(1.0, 1.0, 1.0, 1.0);
          
      glMatrixMode(GL_MODELVIEW);
      glLoadIdentity();
      gluLookAt(2.0, 4.0, 6.0, 0., 0., 0., 0., 1., 0.);

      glRotate(30.0, 0.0, 0.0, 1.0);

      self.texture.bind()

      glBegin(GL_QUADS);


      glTexCoord2f(0.0, 0.0)
      glVertex(-1.0,  1.0, 0.0);

      glTexCoord2f(1.0, 0.0)
      glVertex( 1.0,  1.0, 0.0);

      glTexCoord2f(1.0, 1.0)
      glVertex( 1.0, -1.0, 0.0);

      glTexCoord2f(0.0, 1.0)
      glVertex(-1.0, -1.0, 0.0);


      glEnd();
      
      self.texture.bind()
      
      glFlush()

    def resizeGL(self, width, height):
      if width == 0 or height == 0:
        return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, width/height, 0.5, 100)
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
  
    main_view = MainView(app_name, 40, 40, 480, 480)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

