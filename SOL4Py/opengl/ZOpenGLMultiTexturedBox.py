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
 
#  ZOpenGLMultiTexturedBox.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLTexture2D import *
from SOL4Py.opengl.ZTextureCoordTriangularBox import *
from SOL4Py.opengl.ZOpenGLImageInfo import *


class ZOpenGLMultiTexturedBox(ZOpenGLObject):

  FACES = 6
  

  def __init__(self, w, h, z):
    super().__init__()
    self.texture = []
    self.ttb     = None
    self.w = w
    self.h = h
    self.z = z

  def createTexture(self, size, filenames):
    self.ttb = None

    if size != self.FACES:
      raise ValueError("Invalid size parameter:" + str(size))
   
    if filenames == None:
      raise ValueError("Invalid filenames parameter")
      
    self.textures = []    

    for i in range(self.FACES):
      self.textures.append(ZOpenGLTexture2D())
    
    self.ttb = self.createBox(self.w, self.h, self.z)
    
    self.load(size, filenames)


  def createTextureFromImageInfo(self, size, imageInfos):  # ZOpenGLImageInfo
    self.ttb = None

    if size != self.FACES:
      raise ValueError("Invalid size parameter:" + str(size))
         
    self.textures = []    

    for i in range(self.FACES):
      self.textures.append(ZOpenGLTexture2D())
    
    self.ttb = self.createBox(self.w, self.h, self.z)

    self.setImageInfo(size, imageInfos)


  # Refine your own method in a sublcass derived from this class.  
  def createBox(self, w, h, z):
    return ZTextureCoordTriangularBox(w, h, z)
    
    
  def load(self, size, filenames):

    for i in range(self.FACES): 
      self.textures[i].bind()

      self.textures[i].pixelStore(GL_UNPACK_ALIGNMENT, 1)

      self.textures[i].parameter(GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      self.textures[i].parameter(GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      self.textures[i].env(GL_TEXTURE_ENV_MODE, GL_MODULATE)

      self.textures[i].generate(GL_S, GL_TEXTURE_GEN_MODE, GL_NORMAL_MAP)
      self.textures[i].generate(GL_T, GL_TEXTURE_GEN_MODE, GL_NORMAL_MAP)

      self.textures[i].parameter(GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
      self.textures[i].parameter(GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
      
      self.textures[i].imageFromFile(filenames[i]) # GL_TEXTURE_2D)
    
      self.textures[i].unbind()

  def setImageInfo(self, size, imageInfos):
    if (size != self.FACES) :
      raise ValueError("Invalid size parameter: " + str(size))
    
    if (imageInfos ==  None) :
      raise ValueError("Invalid imageInfos parameter")

    for i in range(self.FACES):
      self.textures[i].bind()

      self.textures[i].pixelStore(GL_UNPACK_ALIGNMENT, 1) ##4)

      self.textures[i].parameter(GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      self.textures[i].parameter(GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      self.textures[i].env(GL_TEXTURE_ENV_MODE, GL_MODULATE)

      self.textures[i].generate(GL_S, GL_TEXTURE_GEN_MODE, GL_NORMAL_MAP)
      self.textures[i].generate(GL_T, GL_TEXTURE_GEN_MODE, GL_NORMAL_MAP)

      self.textures[i].parameter(GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
      self.textures[i].parameter(GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
     
      self.textures[i].imageFromImageInfo(imageInfos[i])
    
      self.textures[i].unbind()


  def draw(self):
  
    box = self.ttb.getBox()
      
    numFaces = self.ttb.getNumberOfFaces()
    numVerticesPerFace = self.ttb.getNumberOfVerticesPerFace()
      
    glEnable(GL_NORMALIZE)
    glEnable(GL_BLEND)
    
    glEnable(GL_TEXTURE_2D)
        
    for i in range(numFaces):
      self.textures[i].bind()
      glBegin(GL_TRIANGLES)

      for j in range(numVerticesPerFace):
        cv = box[i*numFaces + j]
        self.textures[i].coordVertex(cv[0], cv[1])
       
      glEnd()
      self.textures[i].unbind()
          
    glDisable(GL_TEXTURE_2D) 

    glFlush()

 