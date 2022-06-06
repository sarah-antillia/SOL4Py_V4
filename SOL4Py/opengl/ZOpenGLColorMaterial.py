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

#  ZOpenGLColorMaterial.py


# encodig: utf-8

import numpy as np
import math

from ctypes import *

from SOL4Py.opengl.ZOpenGLIndexedVertices import *


class ZOpenGLColorMaterial(ZOpenGLObject):

  ## Constructor
  def __init__(self, face, mode):
    
    self.face = face
    self.mode = mode

    #The parameter face will take CL_FRONT, CL_BACK, CL_FRONT_AND_BACK    
    #The parameter mode will take GL_EMISSION, GL_AMBIENT, GL_DIFFUSE, 
    #GL_SPECULAR, and GL_AMBIENT_AND_DIFFUSE. 
    # The initial value is GL_AMBIENT_AND_DIFFUSE. 

    glColorMaterial(face, mode);


  def enable(self):
    glEnable(GL_COLOR_MATERIAL);


  def disable(self):
    glDisable(GL_COLOR_MATERIAL);
  
