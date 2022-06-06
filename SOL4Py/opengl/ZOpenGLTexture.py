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

#  ZOpenGLTexture.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLTexture(ZOpenGLObject):
  ## Constructor
  def __init__(self, target = GL_TEXTURE_2D):
    super().__init__()
    self.target = target

    glEnable(self.target)

    self.id = glGenTextures(1)
    print(self.id)

  def gettexture(self):
    return self.id


  def bind(self):
    glBindTexture(self.target, self.id)


  def unbind(self):
    glBindTexture(self.target, 0)


  def parameter(self, name, value):
    glTexParameterf(self.target, name, value)


  def getTarget(self):
    return self.target


  def getTexture(self):
    return self.id

  def env(self, name, value):
    glTexEnvf(GL_TEXTURE_ENV, name, value)
 

  def coord1F(self, s):
    glTexCoord1f(s)

 
  def coord2F(self, s, t):
    glTexCoord2f(s, t)


  def coordVertex(self, coord, vertex): #TextureCoord2Vertex3& cube)
    glTexCoord2fv(coord)
    glVertex3fv(vertex)


  
  def coord2F(self, s, t):
    glTexCoord2f(s, t)  


  def coord3F(self, s, t, r):
    glTexCoord3f(s, t, r)


  def coord4F(self, s, t, r, q):
    glTexCoord4f(s, t, r, q)


  def coordFV(self, size, v):
    if size ==1: 
      glTexCoord1fv(v)
    if size == 2:
      glTexCoord2fv(v)
    if size == 3:
      glTexCoord3fv(v)
    if size == 4:
      glTexCoord4fv(v)


  def generate(self, coord, name, param):
    glTexGenf(coord, name, param) 


  def pixelStore(self, name, param): 
    glPixelStorei(name, param)


  def env(self, mode=GL_TEXTURE_ENV_MODE, value=GL_MODULATE):
    glTexEnvf(GL_TEXTURE_ENV, mode, value)
