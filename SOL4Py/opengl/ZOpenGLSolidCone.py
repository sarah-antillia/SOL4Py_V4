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

#  ZOpenGLSolidCone.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLGeometry import *

class ZOpenGLSolidCone(ZOpenGLGeometry):
  
  def __init__(self, materia, base, height, slices, stacks):
    super().__init__(materia)
    
    self.reshape(base, height, slices, stacks)
  
  def reshape(self, base, height, slices, stacks):
    
    self.base   = base
    self.height = height
    self.slices = slices
    self.stacks = stacks
    
  def draw(self): #, x, y, z):
    glPushMatrix()
    #glTranslate(x, y, z)
    self.materialize()
    self.solidCone(self.base, self.height, self.slices, self.stacks)
    glPopMatrix()

