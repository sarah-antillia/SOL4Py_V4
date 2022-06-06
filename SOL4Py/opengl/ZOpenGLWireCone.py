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

#  ZOpenGLWireCone.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLGeometry import *


class ZOpenGLWireCone(ZOpenGLGeometry):

  def __init__(self, materia, base=1.0, height=1.0, slices=32, stacks=32):
    super().__init__(materia)
    self.reshape(base, height, slices, stacks)
  
  
  def reshape(self, base, height, slices, stacks):
    self.base   = base
    self.height = height
    self.slices = slices
    self.stacks = stacks

  def draw(self, x=0.0, y=0.0, z=0.0):
    glPushMatrix()
    glTranslate(x, y, z)
    self.materialize()
    self.wireCone(self.base, self.height, self.slices, self.stacks)

    glPopMatrix()


