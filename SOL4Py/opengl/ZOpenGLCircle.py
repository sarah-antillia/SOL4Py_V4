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

#  ZOpenGLCircle.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLArrayBuffer import *

class ZOpenGLCircle :
  
  def __init__(self, px = 0.0,  py = 0.0, pz = 0.5, radius  = 1.0):
    if radius <= 0.0 :
      raise Exception("Invalid parameter.")
       
    self.createCircle(px, py, pz, radius)


  def createCircle(self, px, py, pz, radius):  
    self.STRIDE       = 3
    self.CIRCLE_ANGLE = 360
    
    self.vertices = [[0.0 for i in range(0, self.STRIDE)] for j in range(0, self.CIRCLE_ANGLE)]

    for i in range(0, self.CIRCLE_ANGLE-1, 2):
        self.vertices[i    ][0] = px + radius * math.cos(math.radians(i    ))
        self.vertices[i    ][1] = py + radius * math.sin(math.radians(i    ))
        self.vertices[i    ][2] = pz
        self.vertices[i + 1][0] = px + radius * math.cos(math.radians(i + 1))
        self.vertices[i + 1][1] = py + radius * math.sin(math.radians(i + 1))
        self.vertices[i + 1][2] = pz

    self.vertexBuffer = ZOpenGLArrayBuffer(GL_ARRAY_BUFFER)
    self.vertexBuffer.bind()
    data  =  np.array(self.vertices, dtype="float32")
    byteSize = self.STRIDE * self.CIRCLE_ANGLE * 4
    
    self.vertexBuffer.data(byteSize, self.STRIDE, self.CIRCLE_ANGLE, data)
    self.vertexBuffer.unbind()

  def getOrbitPosition(self, angle):
    if angle >= self.CIRCLE_ANGLE:
        angle -= self.CIRCLE_ANGLE
    if angle < 0 :
        angle = 0  
    return self.vertices[angle]

  def draw(self):
    self.vertexBuffer.drawArray(GL_LINE_LOOP)

