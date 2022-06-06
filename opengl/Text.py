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

#  Text.py

# encodig: utf-8

import sys

# 
sys.path.append('../')

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLText import *


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
   
      glFrustum(1 , -1 , -1 , 1 , 1 , 10);
      self.text1 = ZOpenGLText("Hello world.") 
      self.text2 = ZOpenGLText("Goodbye world.") 

      w = self.width()
      h = self.height()
      glTranslatef(0.0, h-100.0 , 0);

    def paintGL(self):
      w = self.width()
      h = self.height()
      glMatrixMode(GL_PROJECTION);

      glPushMatrix();

      glLoadIdentity();
      gluOrtho2D(0, w, h, 0);

      glMatrixMode(GL_MODELVIEW);

      glPushMatrix();
      glLoadIdentity();
      scale = 0.2
      #self.text.draw(10, 100, 0, scale, GLUT_BITMAP_TIMES_ROMAN_24)
      self.text1.draw(10, 70, 0,  0.4, GLUT_STROKE_ROMAN)
      self.text2.draw(10, 140, 0, 0.2, GLUT_STROKE_ROMAN)

      glPopMatrix();
      glMatrixMode(GL_PROJECTION);
 
      glPopMatrix();
      glMatrixMode(GL_MODELVIEW);
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

