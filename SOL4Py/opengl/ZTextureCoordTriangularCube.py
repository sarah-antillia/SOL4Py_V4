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

#  ZTextureCoordTriangularCube.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLTexture2D import *
from SOL4Py.opengl.ZTextureCoordTriangularBox import *

class ZTextureCoordTriangularCube(ZTextureCoordTriangularBox):
  
  def __init__(self, size=1.0):
    super().__init__(size, size, size)
       
       