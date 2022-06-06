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

#  ZOpenGLSphere.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLShape import *

class ZOpenGLSphere(ZOpenGLShape):
  
  def __init__(self, quadric, materia=None, radius=1.0, slices=20, stacks=20):
    super().__init__(quadric, materia)
    self.radius = radius
    self.slices = slices
    self.stacks = stacks

  def reshape(self, radius, slices, stacks):
    self.radius = radius
    self.slices = slices
    self.stacks = stacks

  def draw(self):

    gluSphere(self.getQuadric(),
                        self.radius,
                        self.slices,
                        self.stacks);
