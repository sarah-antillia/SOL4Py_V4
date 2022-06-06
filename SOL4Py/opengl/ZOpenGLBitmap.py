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

#  ZOpenGLBitmap.py

# encodig: utf-8

from SOL4Py.ZColor4 import *
from SOL4Py.opengl.ZOpenGLObject import *

class ZOpenGLBitmap(ZOpenGLObject):
  ## Constructor
  def __init__(self, x, y, width, height, 
                    depth, format=GL_RGB, type = GL_UNSIGNED_BYTE):
    super().__init__()
    
    self.x        = x
    self.y        = y
    self.width    = width
    self.height   = height
    self.format   = format
    self.type     = type
    self.channels = 0
    self.depth    = depth
  
    self.channels = 1
    if self.format == GL_RGB:
      self.channels = 3
    elif self.format == GL_RGBA:
      self.channels = 4
    else:
      self.channels = 1


  def readPixels(self, buffer=GL_BACK):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    glReadBuffer(buffer)
    return glReadPixels(self.x, self.y, self.width, self.height, self.format, self.type)
 


