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

#  ZOpenGLTexture2D.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLTexture import *
from SOL4Py.opengl.ZOpenGLImage import *
from SOL4Py.opengl.ZOpenGLImageInfo import *


class ZOpenGLTexture2D(ZOpenGLTexture):

  ## Constructor
  def __init__(self):
    super().__init__(GL_TEXTURE_2D)


  def image(self, level, components,
       width, height, border,
       format, type, pixels):
       
    glTexImage2D(self.getTarget(),
        level, components,
        width, height, border,
        format, type, pixels) 
  
  # Create a texturedImage from an imageInfo (OpenGLImageInfo)
  def imageFromImageInfo(self, imageInfo):
    glTexImage2D(self.getTarget(),
        0, imageInfo.format,
        imageInfo.width, imageInfo.height, 0,
        imageInfo.format, imageInfo.type, imageInfo.imageData) 
    

  def imageFromFile(self, filename, level=0,  border=0, flip=True):
    if filename == None:
      raise ValueError("Invalid argument")

    self.image = ZOpenGLImage(filename, flip)
    w = self.image.width
    h = self.image.height
    glTexImage2D(self.getTarget(), 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)


  def subImage(self, level,  
                xoffset,  
                yoffset,  
                width,  
                height,  
                format,  
                type,  
                data):
    glTexSubImage2D(self.getTarget(), level, xoffset, yoffset, width, height, format, type, data) 


  def subImageFromFile(self, filename, level, xoffset, yoffset):
    if filename == None:
      raise ValueError("Invalid argument")
    
    self.image = ZOpenGLImage(filename)
    w = self.image.width
    h = self.image.height
      
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)
    glTexSubImage2D(self.getTarget(), level, xoffset, yoffset, w, h,  
        GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)


  def mipmap(self, internalFormat, width, height, format, type, data): 
    gluBuild2DMipmaps(self.getTarget(), 
        internalFormat,  
        width,  
        height,  
        format,  
        type,  
        data)


  def mipmapFromFile(self, filename):
    if filename == None:
      raise ValueError("Invalid argument")

    self.image = ZOpenGLImage(filename)
    w = self.image.width
    h = self.image.height

    self.mipmap(GL_RGBA, w, h, GL_RGBA, GL_UNSIGNED_BYTE, self.image.bytes)
 

