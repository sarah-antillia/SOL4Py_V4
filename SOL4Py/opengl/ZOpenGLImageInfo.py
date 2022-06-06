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


#  ZOpenGLImageInfo.py

# encodig: utf-8

import numpy as np

from SOL4Py.opengl.ZOpenGLObject import *
 
class ZOpenGLImageInfo(ZOpenGLObject):

  def __init__(self, xinternal = GL_RGBA, 
                     xformat   = GL_BGRA, 
                     xtype     = GL_UNSIGNED_BYTE):
                     
    self.depth       = 0
    #self.xformat    = 0
    self.internalFormat = xinternal
    self.width          = 0
    self.height         = 0
    self.format         = xformat
    self.type           = xtype
    self.widthStep      = 0
    self.imageSize      = 0
    self.imageData      = None # SmartPtrs<uint32_t>  imageData;

