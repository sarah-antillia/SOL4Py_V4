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

#  ZOpenGLBufferedShape.py

# encodig: utf-8



from SOL4Py.opengl.ZOpenGLIndexedVertices  import *   
from SOL4Py.openglarb.ZOpenGLVertexBufferARB  import *
from SOL4Py.openglarb.ZOpenGLIndexBufferARB  import *
from SOL4Py.opengl.ZOpenGLMateria  import *

class ZOpenGLBufferedShape(ZOpenGLObject):
  ## Constructor  

  def __init__(self, vertices, materia=None):
    super().__init__()
 
    self.vertices = vertices
    self.materia  = materia
    if vertices != None:
      self.vertexBuffer = ZOpenGLVertexBufferARB();
      self.vertexBuffer.bind();
      ver = np.array(vertices.getVertices(), dtype="float32")
      
      self.vertexBuffer.data(vertices.getVerticesDataSize(), ver, GL_STATIC_DRAW_ARB);
      self.vertexBuffer.unbind();
              
      self.indexBuffer = ZOpenGLIndexBufferARB();
      self.indexBuffer.bind();
      ind = np.array(vertices.getIndices(), dtype="int")
      self.indexBuffer.data(vertices.getIndicesDataSize(), ind, GL_STATIC_DRAW_ARB);
      self.indexBuffer.unbind();
    else:
      raise ValueError("Invalid vertices parameter.");


  def draw(self): 
    self.vertexBuffer.bind();
    self.indexBuffer.bind();
    if self.materia != None:
      self.materia.materialize();
    self.vertices. draw();
   
    self.vertexBuffer.unbind();
    self.indexBuffer.unbind();

