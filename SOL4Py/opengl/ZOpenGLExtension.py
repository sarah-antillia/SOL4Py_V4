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

#  ZOpenGLExtension.py

# encodig: utf-8

import sys
import os
import math
import traceback

import numpy as np

import OpenGL
import OpenGL.GL as gl

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

 
class ZOpenGLExtension:

  # ZOpenGLObject Constructor
  def __init__(self):
    self.extensions = glGetString(GL_EXTENSIONS)
    self.extensions = self.extensions.split()
    
    
  def isSupported(self, name):
    name = name.encod("utf-8")
    rc = False
    for extension in self.extensions:
      if extension == name:
        self.SUPPORT_EXTENSION = True
        print("supported " + name)
        rc = True
        break
    return rc
    
  def get_extensions(self):
    extensions = []
    for name in self.extensions:
      extensions.append(str(name))
    return extensions
    
     
  def isGL_ARB_vertex_buffer_object(self):
    return self.isSuppored("GL_ARB_vertex_buffer_object")

