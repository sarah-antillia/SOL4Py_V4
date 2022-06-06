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

#  ZOpenGLMaterial.py

# encodig: utf-8

from SOL4Py.ZColor4 import *
from SOL4Py.opengl.ZOpenGLObject import *

class ZOpenGLMaterial(ZOpenGLObject):

  def __init__(self, face):
    super().__init__()
    #The parameter face will take CL_FRONT, CL_BACK, CL_FRONT_AND_BACK 
    self.face = face


  def ambientv(self, values):
    glMaterialfv(self.face , GL_AMBIENT , values) 
  

  def ambient(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glMaterialfv(self.face , GL_AMBIENT , values) 


  def diffusev(self, values):
    glMaterialfv(self.face , GL_DIFFUSE, values) 
  

  def diffuse(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glMaterialfv(self.face , GL_DIFFUSE, values) 
  

  def specularv(self, values):
    glMaterialfv(self.face , GL_SPECULAR, values) 
  

  def specular(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glMaterialfv(self.face , GL_SPECULAR, values) 


  def shininessv(self, values):
    glMaterialfv(self.face , GL_SHININESS, values) 


  def shininess(self, shine):
    values = [shine]
    glMaterialfv(self.face , GL_SHININESS, values) 


  def emissionv(self, values):
    glMaterialfv(self.face , GL_EMISSION, values) 
  

  def emission(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glMaterialfv(self.face , GL_EMISSION, values) 


  def ambientAndDiffuse(self, values):
    glMaterialfv(self.face, GL_AMBIENT_AND_DIFFUSE, values) 


  def colorIndexes(self, values):
    glMaterialfv(self.face , GL_COLOR_INDEXES, values) 
  

  def colorIndexes(self, r,  g,  b):
    values = [r, g, b] 
    glMaterialfv(self.face, GL_COLOR_INDEXES, values) 
  

