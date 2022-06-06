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

#  MultiColoredTriangleShader.py

# encoding: utf-8

import sys
import os
import traceback

import traceback
import numpy as np
import math

sys.path.append('../')
from PIL import Image, ImageOps

from SOL4Py.opengl.ZOpenGLMainView import *
from SOL4Py.opengl.ZOpenGLArrayBuffer import *
from SOL4Py.opengl2.ZOpenGLVertexShader import *
from SOL4Py.opengl2.ZOpenGLFragmentShader import *
from SOL4Py.opengl2.ZOpenGLProgram import *
from SOL4Py.opengl2.ZOpenGLVertexAttribute import *


class MainView(ZOpenGLMainView):

  ##Inner class starts.
  class OpenGLView(ZOpenGLView):
    
    ## Constructor
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)


    def initializeGL(self):
      glMatrixMode(GL_PROJECTION);
      glLoadIdentity();

      glEnable( GL_DEPTH_TEST );
      glFrustum(1 , -1 , -1 , 1 , 1 , 10);
      glClearColor(0.0, 0.0, 1.0, 1.0);
      self.vertexShader = ZOpenGLVertexShader()
     
      vertShaderSource = "./vertexShader.glsl"
      
      self.vertexShader.load_file(vertShaderSource) 
      self.fragmentShader = ZOpenGLFragmentShader() ;
      fragShaderSource = "./fragmentShader.glsl"
      self.fragmentShader.load_file(fragShaderSource);
      
      self.program = ZOpenGLProgram();
      self.program.attachShader(self.vertexShader);
      self.program.attachShader(self.fragmentShader);

      self.program.link();
      
      self.program.detachShader(self.vertexShader);
      self.program.detachShader(self.fragmentShader);


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glLoadIdentity();
      glClearColor(1.0, 1.0, 1.0, 1.0);

      self.program.use();
    
      glEnableClientState(GL_VERTEX_ARRAY);
      glEnableClientState(GL_COLOR_ARRAY)

      triangles = [
          # coord2d      colors rgb
          [ 0.0,  0.5,   1.0, 1.0, 0.0],
          [-0.5, -0.5,   0.0, 0.0, 1.0],
          [ 0.5, -0.5,   1.0, 0.0, 0.0],
       ];
        
      array = np.array(triangles, dtype="float32")

      buffer = ZOpenGLArrayBuffer()
      buffer.bind();
      buffer.data(4*5*len(triangles), 3, len(triangles), array, GL_STATIC_DRAW);


      coord2d = ZOpenGLVertexAttribute(self.program.getAttributeLocation("coord2d"))
      vcolor  = ZOpenGLVertexAttribute(self.program.getAttributeLocation("v_color"));
        
      coord2d.setPointer(2, GL_FLOAT, GL_FALSE, 4 * 5, None); 
      
      # Please see: https://stackoverflow.com/questions/11132716/how-to-specify-buffer-offset-with-pyopengl
      vcolor.setPointer(3, GL_FLOAT, GL_FALSE,  4 * 5, ctypes.c_void_p(2*4)) 

      glDrawArrays(GL_TRIANGLES, 0, len(triangles));
 
      glDisableClientState(GL_VERTEX_ARRAY);
      glDisableClientState(GL_COLOR_ARRAY)



    def resizeGL(self, width, height):
      side = min(width, height)
      if side < 0: return
      glViewport(0, 0, width, height)
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(50.0, width / height, 0.1, 50.0)

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
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 600, 380)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

