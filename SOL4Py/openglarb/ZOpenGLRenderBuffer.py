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

#  ZOpenGLRenderBuffer.py

# encodig: utf-8
import numpy as np
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.openglarb.ZOpenGLRenderBuffers import *


#ifdef GL_ARB_framebuffer_object


class ZOpenGLRenderBuffer(ZOpenGLRenderBuffers):

  def __init__(self):
    super().__init__(1, GL_RENDERBUFFER)
  
  
  def bind(self):
    if self.size == 1:
      glBindFramebuffer(self.target, self.buffer);


#endif
  
  