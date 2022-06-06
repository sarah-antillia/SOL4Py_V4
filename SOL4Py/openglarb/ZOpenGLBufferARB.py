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

#  ZOpenGLBufferARB.py

# encodig: utf-8
import numpy as np
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *
from OpenGL.GL.ARB.vertex_buffer_object import *

# http://oss.sgi.com/projects/ogl-sample/registry/ARB/vertex_buffer_object.txt


#ifdef GL_ARB_vertex_buffer_object

class ZOpenGLBufferARB(ZOpenGLObject):

  ## Constructor
  def __init__(self, target = GL_ARRAY_BUFFER_ARB):
    super().__init__()
    self.id     = 0
    self.target = target
    self.size   = 0
    self.id     = self.create(1)

    if self.id <=0:
      raise RuntimeError("Failed to create OpenGLBufferARB") 


  def create(self, size):
    return glGenBuffersARB(size)


  def destroy(self):  
    glDeleteBuffersARB(self.size, self.id)


  def bind(self): 
    glBindBufferARB(self.target, self.id)


  def unbind(self):
    glBindBufferARB(self.target, 0)


  def getBufferParameter(self, pname):
    return glGetBufferParameterivARB(self.target, pname)


  def getBufferPointer(self, pname):
    return glGetBufferPointervARB(self. target, pname)


  def data(self, sizei, data, usage=GL_DYNAMIC_DRAW_ARB):
    if sizei > 0 and data.all() != None:
      self.size = sizei
      glBufferDataARB(self.target, sizei, data, usage)


  def subData(self, offset, sizei, data):
    if offset > 0 and sizei > 0 and data != None: 
       glBufferSubDataARB(self.target, offset, sizei, data)



  def getBufferSubData(self, offset, size):
    return glGetBufferSubDataARB(self.target, offset, size)


  def isBuffer(self):
    return glIsBufferARB(self.id)


  def map(self, access):
    glMapBufferARB(self.target, access)


  def unmap(self):
    return glUnmapBufferARB(self.target)


#ifdef GL_ARB_draw_buffers

  def drawBuffers(self, n, bufs):
    self.bind()
    state = OpenGLClientState(GL_VERTEX_ARRAY)
    state.enable()

    glDrawBuffersARB(n, bufs) 

    state.disable()
    self.unbind()


#endif
  
  def drawArray(self, style):
    self.bind()
    
    state = OpenGLClientState(GL_VERTEX_ARRAY)
    state.enable()

    vertexNum = 3
    
    glVertexPointer(vertexNum, GL_FLOAT, 0, 0)
  
    dataNum = self.size / ( vertexNum * 4) # sizeof(GLfloat))
    print("dataNum %d\n", dataNum)
    
    glDrawArrays(style, 0 , dataNum)
    state.disable()
    
    self.unbind()



#endif

