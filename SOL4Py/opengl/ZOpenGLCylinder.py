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

#  ZOpenGLCylinder.py

# encodig: utf-8

import sys

# 

from SOL4Py.opengl.ZOpenGLShape import *


class ZOpenGLCylinder(ZOpenGLShape):
  
  def __init__(self, quadric, materia, base=1.0, top=1.0, height=1.0, slices=40, stacks=40):
    super().__init__(quadric, materia)
    self.reshape(base, top, height, slices, stacks)


  def reshape(self, base, top, height, slices, stacks):
    self.base   = base  
    self.top    = top
    self.height = height
    self.slices = slices
    self.stacks = stacks


  def draw(self):  
    gluCylinder(self.getQuadric(),
          self.base,
          self.top,  
          self.height, 
          self.slices,  
          self.stacks)


  def translate(self, x, y, z):  
      glPushMatrix()
      glTranslate(x, y, z)
      self.materialize()
      gluCylinder(self.getQuadric(),
          self.base,
          self.top,  
          self.height,  
          self.slices,  
          self.stacks)
      glPopMatrix()

