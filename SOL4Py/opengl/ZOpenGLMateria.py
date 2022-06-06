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

#  ZOpenGLMateria.py

# encodig: utf-8

from SOL4Py.ZColor4 import *
from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLMateria(ZOpenGLObject):
  # class variables (static const int) 
    
  AMBIENT   =0x00001
  DIFFUSE   =0x00010
  SPECULAR  =0x00100
  EMISSION  =0x01000
  SHININESS =0x10000
  
  ALL_MATERIAS = (AMBIENT|DIFFUSE|SPECULAR|EMISSION|SHININESS)


  #The face parameter face will take GL_FRONT, GL_BACK, GL_FRONT AND GL_BACK
  def __init__(self, face=0, ambient=[0.0, 0.0, 0.0, 0.0],  diffuse=[0.0, 0.0, 0.0, 0.0],  
           specular=[0.0, 0.0, 0.0, 0.0], emission=[0.0, 0.0, 0.0, 0.0], shininess=0.0):
    super().__init__()
    
    self.face = face
    self.enabled = False
    
    self.initialize()
    self.update(face, ambient,  diffuse,  specular, emission, shininess)

  def  initialize(self):
    self.ambient  = [0.0, 0.0, 0.0, 0.0]
    self.diffuse  = [0.0, 0.0, 0.0, 0.0]
    self.specular = [0.0, 0.0, 0.0, 0.0]
    self.emission = [0.0, 0.0, 0.0, 0.0]

    self.shininess = 0.0


  def update(self, face, ambient,  diffuse,  specular, emission, shininess):
    self.face = face
    self.enabled = True
 
    self.ambient   = ambient
    self.diffuse   = diffuse
    self.specular  = specular
    self.emission  = emission
    self.shininess = shininess


  def copy(self, mat):
    self.initialize()
    self.face      = mat.face
    self.ambient   = mat.ambient
    self.diffuse   = mat.diffuse
    self.specular  = mat.specular
    self.emission  = mat.emission
    self.shininess = mat.shininess
    self.enabled   = mat.enabled


  def enable(self):
    self.enabled = True


  def disable(self):
    self.enabled = False


  def face(self, face):
    self.face = face


  def face():
    return self.face


  def ambient(self, color):
    self.ambient = color


  def ambient(self, value):
    if len(value) == 4:
      self.ambient = value


  def diffuse(self, value):
    if len(value) == 4:
      self.diffuse = value


  def specular(self, value):
    if len(value) == 4:
      self.specular = value



  def shininess(self, shine):
    self.shininess = shine


  def emission(self, color):
    self.emission = color



  def materialize(self, flags=ALL_MATERIAS):
    if self.enabled == True:
      if flags &  self.AMBIENT: 
        if self.ambient != None:
          glMaterialfv(self.face , GL_AMBIENT , self.ambient)# value) 
      
      if flags & self.DIFFUSE:
        if self.diffuse != None:
          glMaterialfv(self.face , GL_DIFFUSE, self.diffuse) 
      
      if flags & self.SPECULAR: 
        if self.specular != None:
          glMaterialfv(self.face , GL_SPECULAR, self.specular) 
      
      if flags & self.EMISSION: 
        if self.emission != None:
          glMaterialfv(self.face , GL_EMISSION, self.emission)    
      
      if flags & self.SHININESS:
        glMaterialfv(self.face , GL_SHININESS,[self.shininess]) 
      
