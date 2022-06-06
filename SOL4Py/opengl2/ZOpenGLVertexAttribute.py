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

#  ZOpenGLVertexAttribute.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl2.ZOpenGLProgram import *

class ZOpenGLVertexAttribute(ZOpenGLObject):
 
#ifdef GL_VERSION_2_0


  def __init__(self, index, onoff=True):
    super().__init__()
  
    self.index  = index
    self.enable = onoff
  
    if self.index < 0: 
      raise ValueError("Invalid attribute index: " + str(index)) 
    
    if self.enable: 
      self.enableArray()
    else:
      self.disableArray()

  def disableArray(self):
    glDisableVertexAttribArray(self.index)


  def enableArray(self):
    glEnableVertexAttribArray(self.index)


  def getPointer(self, pname):
    return glGetVertexAttribPointerv(self.index, pname) 


  def getVertexAttributefv(self, pname):
    return glGetVertexAttribdfv(self.index, pname)


  def vertexAttribute1d(self, x):
    glVertexAttrib1d(self.index, x)


  def setfv(self, v, size):
    if v == None :
      raise ValueError("Invalid value parameter.")
    
    if size < 1 or size > 4: 
      raise ValueError("Invalid size parameter.")
    
    if size == 1:
      self.set1f(v)
    elif size ==2 :
      self.set2f(v)
    elif size == 3:
      self.set3f(v)
    elif sisze ==4:
      self.set4f(v)



  def set1f(self, x):
    glVertexAttrib1f(self.index, float(x))


  def set1fv(self, v):
    fv = np.array(v, dtype=float)
    glVertexAttrib1fv(self.index, fv)


  def set2f(self, x, y):
    glVertexAttrib2f(self.index, float(x), float(y))


  def set2fv(self, v):
    fv = np.array(v, dtype=float)
    glVertexAttrib2fv(self.index, fv)


  def set3f(self, x, y, z):
    glVertexAttrib3f(self.index, float(x), float(y), float(z))


  def set3fv(self, v):
    fv = np.array(v, dtype=float)
    glVertexAttrib3fv(self.index, fv)


  def set4Niv(self, v):
    iv = np.array(v, dtype=int)
    glVertexAttrib4Niv(self.index, iv)


  def set4f(self, x, y, z, w):
    glVertexAttrib4f(self.index, float(x), float(y), float(z), float( w))


  def set4fv(self, v):
    fv = np.array(v, dtype=float)
    glVertexAttrib4fv(self.index, fv)


  def setPointer(self, size, type, normalized, stride, pointer):
    glVertexAttribPointer(self.index, size, type, normalized, stride, pointer)

#endif

#ifdef GL_VERSION_3_0

  def getI1iv(self, pname):
    return glGetVertexAttribIiv(self.index, pname)


  def setiv(self, v, size):
    if v == None: 
      raise ValueError("Invalid value parameter.")

    if  size <= 0 or size >4: 
      raise ValueError("Invalid size parameter.")

    if size == 1:
      self.setI1iv(v)

    elif size == 2:
      self.setI2iv(v)

    elif size == 3:
      self.setI3iv(v)

    elif size == 4:
      self.setI4iv(v)


  def setI1i(self, v0):
    glVertexAttribI1i(self.index, int(v0))


  def setI1iv(self, v):
    iv = np.array(v, dtype=int)
    glVertexAttribI1iv(self.index, iv)


  def setI2i(self, v0, v1):    
    glVertexAttribI2i(self.index, int(v0), int(v1))


  def setI2iv(self, v):
    iv = np.array(v, dtype=int)
    glVertexAttribI2iv(self.index, iv)


  def setI3i(self, v0, v1, v2):
    glVertexAttribI3i(self.index, int(v0), int(v1), int(v2))


  def setI3iv(self, v):
    iv = np.array(v, dtype=int)  
    glVertexAttribI3iv(self.index, iv)


  def setI4i(self, v0, v1, v2, v3):
    glVertexAttribI4i(self.index, int(v0), int(v1), int(v2), int(v3))


  def setI4iv(self, v):
    iv = np.array(v, dtype=int)
    glVertexAttribI4iv(self.index, iv)



  def setIPointer(self, size, type, stride, pointer):
    glVertexAttribIPointer(self.index, size, type, stride, pointer)


#endif

#ifdef GL_VERSION_3_3
  def divisor(self, div):    
    glVertexAttribDivisor(self.index, div)
  
#endif




