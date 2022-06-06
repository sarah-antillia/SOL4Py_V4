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

#  ZOpenGLFog.py

# encodig: utf-8

import sys

# 

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLFog(ZOpenGLObject):

  def __init__(self):
    super().__init__()


  def enable(self):
    glEnable(GL_FOG)


  def disable(self):
    glDisable(GL_FOG)

 
  #mode = GL_LINEARr, AGL_EXP, AGL_EXP2 
  def mode(self,  mode = GL_LINEAR):
    glFogi(GL_FOG_MODE, mode)


  def density(self,  value):
    glFogf(GL_FOG_DENSITY, value)


  #Specify start position for GL_LINEAR mode
  def start(self,  value):
    glFogf(GL_FOG_START, value)


  #Specify end position for GL_LINEAR mode
  def end(self,  value):
    glFogf(GL_FOG_END, value)


  #Specify color index
  def index(self,  value):
    glFogf(GL_FOG_INDEX, value)


  #Specify color index
  def color(self, value):
    glFogfv(GL_FOG_COLOR, value)


  def color(self,  r,  g,  b,  a):
    value = [r, g, b, a]
    glFogfv(GL_FOG_COLOR, value)


  #def color(self, value):
  #  glFogiv(GL_FOG_COLOR, value)
  



