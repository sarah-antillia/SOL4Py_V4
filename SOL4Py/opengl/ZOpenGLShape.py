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

#  ZOpenGLShape.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.opengl.ZOpenGLQuadric import *


class ZOpenGLShape(ZOpenGLObject):
  
  #OpenGLShape(OpenGLQuadric quardic, ZOpenGLMateria materia)
  def __init__(self, quadric, materia=None):
    super().__init__()
    self.quadric = quadric
    self.materia = materia


  def getQuadric(self): 
    return self.quadric.getQuadric()  # GluQuadric

  def materialize(self, flags=ZOpenGLMateria.ALL_MATERIAS):
    self.materia.materialize(flags);

  # Define your own draw method in a subclass derived from this class.
  def draw(self):
    pass  


