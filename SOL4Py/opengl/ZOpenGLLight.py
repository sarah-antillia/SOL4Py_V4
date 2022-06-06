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

#  ZOpenGLLight.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLMateria import *


class ZOpenGLLight(ZOpenGLObject):

  def __init__(self, light=GL_LIGHT0):
    super().__init__()
    self.light = light
    #The light parameter will take GL_LIGHT0 to GL_LIGHT7
    glEnable(GL_LIGHTING)
    glEnable(self.light)
 
  def enable(self):
    glEnable(self.light)


  def ambientv(self, values):
    glLightfv(self.light, GL_AMBIENT, values)


  def ambient(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glLightfv(self.light, GL_AMBIENT, values)


  def specularv(self, values):
    glLightfv(self.light,GL_SPECULAR, values)


  def specular(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glLightfv(self.light,GL_SPECULAR, values)


  def diffusev(self, values):
    glLightfv(self.light, GL_DIFFUSE, values)


  def diffuse(self, r,  g,  b,  a):
    values = [r, g, b, a]
    glLightfv(self.light, GL_DIFFUSE, values)


  def positionv(self, values):
    glLightfv(self.light,GL_POSITION, values)


  def position(self, x,  y,  z,  w):
    values = [x, y, z, w]
    glLightfv(self.light,GL_POSITION, values)


  def spotDirection(self, values):
    glLightfv(self.light , GL_SPOT_DIRECTION , values) 


  def spotDirection(self, x,  y,  z):
    values = [x, y, z]
    glLightfv(self.light , GL_SPOT_DIRECTION , values) 


  def spotExponent(self, values):
    glLightfv(self.light , GL_SPOT_EXPONENT , values) 


  def spotExponent(self, v):
    values = [v]
    glLightfv(self.light , GL_SPOT_EXPONENT , values) 


  def spotCutoff(self, value):
    glLightfv(self.light , GL_SPOT_CUTOFF, value) 


  def spotCutoff(self, v):
    value = [v]
    glLightfv(self.light , GL_SPOT_CUTOFF, value) 


  def constantAttenuation(self, value):
    glLightfv(self.light , GL_CONSTANT_ATTENUATION, value) 


  def constantAttenuation(self, v):
    glLightfv(self.light , GL_CONSTANT_ATTENUATION, value) 


  def linearAttenuation(self, value):
    glLightfv(self.light , GL_LINEAR_ATTENUATION, value) 


  def linearAttenuation(self, v):
    value = [v]
    glLightfv(self.light , GL_LINEAR_ATTENUATION, value) 


  def quadraticAttenuation(self, value):
    glLightfv(self.light , GL_QUADRATIC_ATTENUATION, value) 


  def quadraticAttenuation(self, v):
    value = [v]
    glLightfv(self.light , GL_QUADRATIC_ATTENUATION, value) 

