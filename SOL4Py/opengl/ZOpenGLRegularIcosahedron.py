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

#  ZOpenGLRegularIcosahedron.py

# Icosahedron's vertices data used here is based on the following webstie 
#
# https:#en.wikipedia.org/wiki/Platonic_solid

# encodig: utf-8

import numpy as np
import math

from ctypes import *

from SOL4Py.opengl.ZOpenGLIndexedVertices import *

  
# 2016/08/10 Icosahedron's vertices data used here is based on the following webstie 
#
# https:#en.wikipedia.org/wiki/Platonic_solid


class ZOpenGLRegularIcosahedron(ZOpenGLIndexedVertices):

  STRIDE   = 6
  FACES    = 20
  VERTICES = 12
  
  # Constructor
  def __init__(self):
    super().__init__()
    self.vertices = None
    self.verticesDataSize = 0
    self.indices  = None
    self.indicesDataSize  = 0
    
    
    g = (1.0 + math.sqrt(5.0))/2.0 #golden ratio

    self.vertices = [
      # X,      Y,  Z
      # 12 vertices
      0.0, -1.0,  -g   ,
      0.0, +1.0,  -g   , 
      0.0, -1.0,  +g   , 
      0.0, +1.0,  +g   ,
      
      -g,     0.0, -1.0, 
      -g,     0.0, +1.0, 
      +g,     0.0, -1.0, 
      +g,     0.0, +1.0,
      
      -1.0, -g,     0.0, 
      +1.0, -g,     0.0, 
      -1.0, +g,     0.0, 
      +1.0, +g,     0.0,
     ]
    
    self.verticesDataSize = len(self.vertices) * 4
    self.numberOfVertices = len(self.vertices)

    self.indices = [    
    #20 faces
     0,  1,  6,
     1,  0,  4,
     2,  3,  5,
     3,  2,  7,
     4,  5, 10,
     5,  4,  8,
     6,  7,  9,
     7,  6, 11,
     8,  9,  2,
     9,  8,  0, 
    10, 11,  1,
    11, 10,  3,
      
     0,  6,  9,
     0,  8,  4, 
     1,  4, 10,
     1, 11,  6,
     2,  5,  8,
     2,  9,  7, 
     3,  7, 11,
     3, 10,  5
    ]
    
    self.indicesDataSize = len(self.indices) * 4
    
    self.numberOfIndices = len(self.indices)
 
      
    
  def getInterleavedArraysFormat(self):
    return GL_V3F
 
  
  def getPrimitiveType(self):
    return GL_POLYGON
 
  
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
  