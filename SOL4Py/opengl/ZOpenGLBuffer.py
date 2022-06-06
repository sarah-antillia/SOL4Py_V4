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

#  ZOpenGLBuffer.py

# encodig: utf-8

import numpy as np
from ctypes import *

from SOL4Py.opengl.ZOpenGLObject import *

class ZOpenGLBuffer(ZOpenGLObject) :
  
  def __init__(self, target=GL_ARRAY_BUFFER):
    super().__init__()
    
    self.id       = 0
    self.target   = target
    self.type     = GL_FLOAT
    self.byteSize = 0
    self.count    = 0
    self.stride   = 0
  
    self.id = glGenBuffers(1)


  def delete(self):
    glDeleteBuffers(1, self.id)

  def bind(self): 
    glBindBuffer(self.target, self.id)

  def unbind(self): 
    glBindBuffer(self.target, 0)

  def data(self, sizei, stride, count, data, usage=GL_DYNAMIC_DRAW):
      #if sizei > 0 and data.all() != None:
      self.byteSize = sizei
      self.stride   = stride
      self.count    = count
      glBufferData(self.target, self.byteSize, data, usage)

  def subData(self, offset, sizei, data):
    if offset > 0 and sizei > 0 and data.all() != None:
      glBufferSubData(self.target, offset, sizei, data)
  

  def drawArray(self, style):
    self.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    
    # Don't call glVertexPointer(self.stride, self.type, 0, 0)
    glVertexPointer(self.stride, self.type, 0, None)
    glDrawArrays(style, 0, self.count)

    glDisableClientState(GL_VERTEX_ARRAY)
    self.unbind()

  

