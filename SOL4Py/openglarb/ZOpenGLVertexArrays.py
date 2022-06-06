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

#  ZOpenGLVertexArrays.py

# encodig: utf-8


from SOL4Py.opengl.ZOpenGLObject import *
from OpenGL.GL.ARB.vertex_array_object import *


#ifdef GL_ARB_vertex_array_object

class ZOpenGLVertexArrays(ZOpenGLObject):
  
  def __init__(self, size):
    super().__init__(1)
    self.size = size
    self.buffer = glGenVertexArrays(self.size)


  def delete(self):
    glDeleteVertexArrays(self.size, self.buffer);


  def getNth(self, i):
    if i >= 0 and i < size:
      return self.ids[i];
    else:
      raise ValueError("Invalid argument " + str(i)); 
  
  def getSize(self):
    return self.size;
 
  
  def bindNth(self, n):
    if n >= 0 and n < size:
      glBindVertexArray(self.ids[n]);
    else:
      raise ValueError("Invalid argument " + str(n)); 
 

  def unbind(self):
    glBindVertexArray(0);

  def isVertexArray(self, n):
    return glIsVertexArray(n);
 

#endif

