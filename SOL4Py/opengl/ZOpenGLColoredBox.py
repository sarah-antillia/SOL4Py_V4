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

#  ZOpenGLColoredBox.py

# encodig: utf-8

import numpy as np
from ctypes import *

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLIndexedVertices import *


class ZOpenGLColoredBox(ZOpenGLIndexedVertices):

  STRIDE   = 6
  FACES    = 6
  VERTICES = 24
  VERTICES_PER_FACE = 24

  # Constructor
  
  def __init__(self, colors=None, numColors=0, x=1.0, y=1.0, z=1.0):
    super().__init__()

    self.vertices         = None
    self.verticesDataSize = 0
    self.indices          = None
    self.indicesDataSize  = 0

    self.vertices = [
      # R,  G,  B,     X,  Y,  Z
      # face 1: 
      1.0, 0.0, 0.0,   x,  y,  z,
      1.0, 0.0, 0.0,  -x,  y,  z,
      1.0, 0.0, 0.0,   x, -y,  z,
      1.0, 0.0, 0.0,  -x, -y,  z,

      # face 2: 
      0.0, 1.0, 0.0,   x,  y,  z,
      0.0, 1.0, 0.0,   x, -y,  z,
      0.0, 1.0, 0.0,   x,  y, -z,
      0.0, 1.0, 0.0,   x, -y, -z,
   
      # face 3: 
      0.0, 0.0, 1.0,   x,  y,   z,
      0.0, 0.0, 1.0,   x,  y,  -z,
      0.0, 0.0, 1.0,  -x,  y,   z,
      0.0, 0.0, 1.0,  -x,  y,  -z,
        
      # face 4: 
      1.0, 1.0, 0.0,   x,  y,  -z,
      1.0, 1.0, 0.0,   x, -y,  -z,
      1.0, 1.0, 0.0,  -x,  y,  -z,
      1.0, 1.0, 0.0,  -x, -y,  -z,

      # face 5: 
      0.0, 1.0, 1.0,  -x,  y,  z,
      0.0, 1.0, 1.0,  -x,  y, -z,
      0.0, 1.0, 1.0,  -x, -y,  z,
      0.0, 1.0, 1.0,  -x, -y, -z,

      # face 6: 
      1.0, 0.0, 1.0,   x, -y,  z,
      1.0, 0.0, 1.0,  -x, -y,  z,
      1.0, 0.0, 1.0,   x, -y, -z,
      1.0, 0.0, 1.0,  -x, -y, -z,
    ]

    self.verticesDataSize = len(self.vertices) * 4
    self.numberOfVertices = len(self.vertices)
    print("self.numberOfVertices " + str(self.numberOfVertices))
    
    if colors != None and numColors == self.FACES:
      self.setFaceColors(colors, numColors)

    if colors != None and numColors == self.VERTICES:
      self.setVerticesColors(colors, numColors)

    self.indices = [ 
      # face 1: 
       0, 1, 2,  2, 1, 3,  
      # face 2: 
       4, 5, 6,  6, 5, 7, 
      # face 3: 
       8, 9,10, 10,9,11, 
      # face 4: 
      12,13,14, 14,13,15,
      # face 5: 
      16,17,18, 18,17,19,  
      # face 6: 
      20,21,22, 22,21,23,  
      ] 
      
    self.indicesDataSize = len(self.indices) * 4
    self.numberOfIndices = len(self.indices)



  def setFaceColors(self, colors, numColors): ##Color3<GLfloat>* colors, int numColors)
   
    if colors !=None and numColors == self.FACES:
      for i in range(numColors):
       for j in range(4) :
        self.vertices[i * self.VERTICES_PER_FACE + j* self.STRIDE + 0] = colors[i][0]
        self.vertices[i * self.VERTICES_PER_FACE + j* self.STRIDE + 1] = colors[i][1]
        self.vertices[i * self.VERTICES_PER_FACE + j* self.STRIDE + 2] = colors[i][2]
    else:
      print("setFaceColors: Invalid face colors")

  def setVerticesColors(self, colors, numColors): ##Color3<GLfloat>* colors, int numColors)
    if colors != None and numColors == self.VERTICES:
      for i in range(numColors):
        self.vertices[i * self.STRIDE + 0] = colors[i][0] #.r
        self.vertices[i * self.STRIDE + 1] = colors[i][1] #.g
        self.vertices[i * self.STRIDE + 2] = colors[i][2] #.b
    else:
      print("setFaceColors: Invalid vertices colors")
 
 
  def getInterleavedArraysFormat(self):
    return GL_C3F_V3F


  def getPrimitiveType(self):
    return GL_TRIANGLES


  def getVertices(self):
    return self.vertices


  def getVerticesDataSize(self):
    return self.verticesDataSize


  def getNumberOfVertices(self):
    return self.numberOfVertices


  def getIndices(self):
    return self.indices


  def getIndicesDataSize(self):
    return self.indicesDataSize
 
  
  def getNumberOfIndices(self):
    return self.numberOfIndices
 
  
  def draw(self):
    glInterleavedArrays(self.getInterleavedArraysFormat(), 0, None)
    glDrawElements(self.getPrimitiveType(), self.getNumberOfIndices(), GL_UNSIGNED_INT, None)
  