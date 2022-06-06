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

#  TriangleShader.py

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
     
      vertShaderSource = "attribute mediump vec4 pos;" \
        "void main() {" \
        "  gl_Position = pos;" \
        "}";
 
      self.vertexShader.load_string(vertShaderSource) 
      self.fragmentShader = ZOpenGLFragmentShader() ;
      fragShaderSource = "void main() {" \
        "  gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);"\
        "}";
      self.fragmentShader.load_string(fragShaderSource);
      
      self.program = ZOpenGLProgram();
      self.program.attachShader(self.vertexShader);
      self.program.attachShader(self.fragmentShader);

      self.program.link();
      
      self.program.detachShader(self.vertexShader);
      self.program.detachShader(self.fragmentShader);


    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      glLoadIdentity();

      self.program.use();
    
      glEnableClientState(GL_VERTEX_ARRAY);
     
      vertices = [ 
        -0.5, 0.5, 0.0, 
         0.5, 0.5, 0.0, 
         0.5,-0.5, 0.0,
        -0.5,-0.5, 0.0
      ]
      pos = self.program.getAttributeLocation("pos");
      attribute = ZOpenGLVertexAttribute(pos);

      attribute.setPointer(3, GL_FLOAT, GL_FALSE, 0, vertices);
      pos = self.program.getAttributeLocation("pos");
      array = np.array(vertices, dtype="float32")
      attribute.setPointer(3, GL_FLOAT, GL_FALSE, 0, array);
    
      glDrawArrays(GL_QUADS, 0, 4);

      glDisableClientState(GL_VERTEX_ARRAY);


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

