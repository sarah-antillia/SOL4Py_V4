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

#  ZOpenGLRenderBuffers.py

# encodig: utf-8
import numpy as np
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *
#from OpenGL.GL.ARB.render_buffer_object import *
from OpenGL.GL.ARB.vertex_buffer_object import *


class ZOpenGLRenderBuffers(ZOpenGLObject):

  def __init__(self, size, target=GL_RENDERBUFFER):
    self.size    = size
    self.target  = target
    self.buffers = None
    if size < 1:
      raise ValueError("Invalid parameters. size " + str(size))
    
    self.buffers = glGenRenderbuffers(self.size)


  def delete(self):
    glDeleteRenderbuffers(self.size, self.buffers)
  

  def bind(self, n=0):
    if self.size == 1:
      glBindRenderbuffer(self.target, self.buffers)
    elif n > 0 and n < self.size:
      glBindRenderbuffer(self.target, self.buffers[n])
    else:
      raise ValueError("Invalid index " + str(n)) ;

        
  def unbind(self):
    glBindRenderbuffer(self.target, 0)

 
  def get(self, n=0):
    if self.size == 1:
      return self.buffers
    elif n >0 and  n < size:
      return self.buffers[n] 
    else:
      raise ValueError("Invalid nth parameter " + str(n))


  def getParameteriv(pname):
    return glGetRenderbufferParameteriv(self.target, pname)


  def isRenderbuffer(self, buffer):
    return glIsRenderbuffer(buffer)


  def storage(self, internalformat, width, height):
    glRenderbufferStorage(self.target, internalformat, width, height)

#endif
  
  