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

#  ZOpenGLTexturedTorus.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLQuadric import *
from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.opengl.ZOpenGLTexture2D import *
import math


class ZOpenGLTexturedTorus(ZOpenGLTexture2D):

  def __init__(self, filename=None, materia=None, r = 0.1, c = 0.2,
                                             r_seg = 40, c_seg=20):

    super().__init__()
    self.materia = materia

    self.r = r
    self.c = c
    
    self.r_seg = r_seg
    self.c_seg = c_seg
    if filename != None:
      self.load(filename)


  def load(self, filename, flip=True):
    self.bind()

    self.pixelStore(GL_UNPACK_ALIGNMENT, 4)
    
    self.parameter(GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    self.parameter(GL_TEXTURE_MIN_FILTER, GL_NEAREST)
  
    self.parameter(GL_TEXTURE_WRAP_S, GL_REPEAT)
    self.parameter(GL_TEXTURE_WRAP_T, GL_REPEAT)
    self.env(GL_TEXTURE_ENV_MODE, GL_MODULATE)

   
    self.imageFromFile(filename, 0, 0, flip=False)

    self.unbind()


  # This is based on the following c code:
  # https://gist.githubusercontent.com/gyng/8939105/raw/254c247610dfdf6f3369035f59dc06f78c65a7c5/torus.cpp

  def draw(self):
    self.bind()
    glFrontFace(GL_CW)
    glEnable(GL_NORMALIZE)

    pi2 = 2.0 * math.pi

    for i in range(self.r_seg):
      glBegin(GL_QUAD_STRIP)
      for j in range(self.c_seg+1):
        for k in range(2):
          s = (i + k) % self.r_seg + 0.5
          t = j % (self.c_seg + 1)

          x = (self.c + self.r * math.cos(s * pi2 / self.r_seg)) * math.cos(t * pi2 / self.c_seg)
          y = (self.c + self.r * math.cos(s * pi2 / self.r_seg)) * math.sin(t * pi2 / self.c_seg)
          z = self.r * math.sin(s * pi2 / self.r_seg )

          u = (i + k) / self.r_seg
          v = t / self.c_seg

          glTexCoord2f(u, v)
          glNormal3f(2 * x, 2 * y, 2 * z)
          glVertex3f(2 * x, 2 * y, 2 * z)
    
      glEnd()
      
    glDisable(GL_NORMALIZE)

    self.unbind()
      
