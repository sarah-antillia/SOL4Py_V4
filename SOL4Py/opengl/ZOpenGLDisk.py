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

#  ZOpenGLDisk.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLShape import *


class ZOpenGLDisk(ZOpenGLShape):
  
  def __init__(self, quadric, materia, inner=0.5, outer=1.0, slices=32, stacks=32):
    super().__init__(quadric, materia)
    self.reshape(inner, outer, slices, stacks)


  def reshape(self, inner, outer, slices, stacks):
    self.inner  = inner  
    self.outer  = outer  
    self.slices = slices
    self.stacks = stacks 


  def draw(self):
    gluDisk(self.quadric.getQuadric(),  
         self.inner,  
         self.outer,  
         self.slices,  
         self.stacks); 

