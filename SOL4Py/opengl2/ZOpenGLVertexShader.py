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

#  ZOpenGLVertexShader.py

# encoding: utf-8

import sys
import os
import traceback

import traceback
import numpy as np
import math
#import OpenGL

from SOL4Py.opengl2.ZOpenGLShader import *


#ifdef GL_VERSION_2_0


class ZOpenGLVertexShader(ZOpenGLShader): 
  ## Constructor
  def __init__(self):
    super().__init__(GL_VERTEX_SHADER)
  


#endif
