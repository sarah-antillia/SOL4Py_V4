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

#  VertexAndIndexBufferARB.py

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
from SOL4Py.opengl.ZOpenGLLight import *
from SOL4Py.opengl.ZOpenGLMaterial import *

from SOL4Py.opengl.ZOpenGLClientState import *
from SOL4Py.openglarb.ZOpenGLBufferedShape import *

from SOL4Py.openglarb.ZOpenGLVertexBufferARB import *
from SOL4Py.openglarb.ZOpenGLIndexBufferARB import *


class MainView(ZOpenGLMainView):

  # Inner class starts.
  class OpenGLView(ZOpenGLView):

    ## Constructor
    def __init__(self, parent=None):
      self.parent = parent
      super(ZOpenGLView, self).__init__(parent)


    def initializeGL(self):

      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()

      glEnable( GL_DEPTH_TEST )

      #  ColorNormalVertex<float,4,3,3> 
      vertices= [
  	     [ 0.5, 0.0, 0.0, 0.5,  -0.6,  0.6,  0.6,  -0.5,  0.5,  0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,  -0.6, -0.6,  0.6,  -0.5, -0.5,  0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,   0.6,  0.6,  0.6,   0.5,  0.5,  0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,   0.6, -0.6,  0.6,   0.5, -0.5,  0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,   0.6,  0.6, -0.6,   0.5,  0.5, -0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,   0.6, -0.6, -0.6,   0.5, -0.5, -0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,  -0.6,  0.6, -0.6,  -0.5,  0.5, -0.5 ],
  	     [ 0.5, 0.0, 0.0, 0.5,  -0.6, -0.6, -0.6,  -0.5, -0.5, -0.5 ],
        ]

      indices = [
         0, 2, 3, 1,	
         2, 4, 5, 3,	
         4, 6, 7, 5,	
         6, 0, 1, 7,	
         6, 4, 2, 0,	
         1, 3, 5, 7,	
        ]

      self.n_vertices = len(vertices)

      self.vertexBuffer = ZOpenGLVertexBufferARB()

      self.vertexBuffer.bind()
      float32_bsize = 4
      data_size = self.n_vertices * (4 + 3 + 3) * float32_bsize
      varray    = np.array(vertices, dtype="float32")
      self.vertexBuffer.data(data_size, varray,  GL_STATIC_DRAW_ARB)
      self.vertexBuffer.unbind()
                
      self.n_indices= len( indices )

      self.indexBuffer  =ZOpenGLIndexBufferARB()
      self.indexBuffer.bind()
      iarray = np.array(indices, dtype="int32")
      self.indexBuffer.data(self.n_indices*4, iarray, GL_STATIC_DRAW_ARB)
      
      self.indexBuffer.unbind()
      self.light = ZOpenGLLight(GL_LIGHT0)
      self.material = ZOpenGLMaterial(GL_FRONT_AND_BACK )
   

    def paintGL(self):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glLoadIdentity()

      glTranslate(0.0,0.0,-1.0)  
      gluLookAt(2.0, 4.0, 6.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0) 
      glClearColor(1.0, 0.8, 0.8, 1.0)
                
      state1 = ZOpenGLClientState(GL_VERTEX_ARRAY) 
      state2 = ZOpenGLClientState(GL_COLOR_ARRAY)
      state3 = ZOpenGLClientState(GL_NORMAL_ARRAY)
      state1.enable()
      state2.enable()
      state3.enable()
      
      lightPosition = [  5.0,  5.0, -8.0 , 1.0 ]
      lightColor    = [  1.0,  0.0,  0.0 , 1.0 ]
      materialColor = [  0.8,  0.8,  0.4 , 1.0 ]

      glEnable(GL_LIGHTING)
      self.light.positionv(lightPosition)
      self.light.diffusev(lightColor)
      self.light.enable() 

      self.material.diffusev(materialColor)

      self.vertexBuffer.bind()
      self.indexBuffer.bind()

      glInterleavedArrays(GL_C4F_N3F_V3F, 0, None)
      glDrawElements(GL_QUADS, self.n_indices, GL_UNSIGNED_INT, None)

      state1.disable()
      state2.disable()
      state3.disable()

      self.vertexBuffer.unbind()
      self.indexBuffer.unbind()

    def resizeGL(self, w,  h):
      if w == 0 or h == 0:
        return
      
      glMatrixMode(GL_PROJECTION)
      glLoadIdentity()
      gluPerspective(16.0, w / h, 0.5, 40.0) 
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

