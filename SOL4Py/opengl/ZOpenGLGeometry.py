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

#  ZOpenGLGeometry.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLMateria import *


class ZOpenGLGeometry(ZOpenGLObject):

  def __init__(self, materia): #OpenGLMateria& materia)
    self.materia = materia

  def draw(x, y, z):
    pass
  
  def  wireCube(self, size):
    glutWireCube(size)
  

  def  solidCube(self, size):
    glutSolidCube(size)
  

  def  wireSphere(self, radius, slices, stacks):
    glutWireSphere(radius, slices, stacks)
  

  def  solidSphere(self, radius, slices, stacks):
    glutSolidSphere(radius, slices, stacks)
  

  def  wireCone(self, base, height, slices, stacks):
    glutWireCone(base, height, slices, stacks)
  

  def  solidCone(self, base, height, slices, stacks):
    glutSolidCone(base, height, slices, stacks)
  

  def  wireTorus(self, innerRadius, outerRadius, sides, rings):
    glutWireTorus(innerRadius, outerRadius, sides, rings)
  

  def  solidTorus(self, innerRadius, outerRadius, sides,  rings):
    glutSolidTorus(innerRadius, outerRadius, sides, rings)
  

  def  wireTeapot(self, value):
    glutWireTeapot(value)

  def  solidTeapot(self, value):
    glutSolidTeapot(value)
  

  def materialize(self, flags=ZOpenGLMateria.ALL_MATERIAS):
    if self.materia != None:
      self.materia.materialize(flags)
  
  
  def ambient(self,color):
    if self.materai != None:
      self.materia.ambient(color)
  

  def ambient(self, value):
    if self.materai != None:
      self.materia.ambient(value)
  

  def ambient(self, r, g, b, a):
    if self.materai != None:
      self.materia.ambient(r, g, b, a)


  def diffuse(self, color):
    if self.materai != None:
      self.materia.diffuse(color)


  def diffuse(self, value):
    if self.materai != None:
      self.materia.diffuse(value)
  

  def diffuse(self,  r,  g,  b,  a):
    if self.materai != None:
      self.materia.diffuse(r, g, b, a)
  

  def specular(self, color):
    if self.materai != None:
      self.materia.specular(color)
  

  def specular(self, value):
    if self.materai != None:
      self.materia.specular(value)
  

  def specular(self, r,  g,  b,  a):
    if self.materai != None:
      self.materia.specular(r, g, b, a)
  

  def shininess(self, shine):
    if self.materai != None:
      self.shininess(shine)
  

  def emission(self, color):
    if self.materai != None:
      self.materia.emission(color)
  

  def emission(self, value):
    if self.materai != None:
      self.materia.emission(value, size)
  

  def emission(self, r,  g,  b,  a):
    if self.materai != None:
      self.materia.emission(r, g, b, a)
  
  
  def draw(self, x, y, z):
    pass
    
