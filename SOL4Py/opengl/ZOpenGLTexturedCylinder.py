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

#  ZOpenGLTexturedCylinder.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLQuadric import *
from SOL4Py.opengl.ZOpenGLMateria import *
from SOL4Py.opengl.ZOpenGLTexture2D import *
from SOL4Py.opengl.ZOpenGLCylinder import *
import math


class ZOpenGLTexturedCylinder(ZOpenGLTexture2D):

  def __init__(self, filename, materia=None, base=2.0,  top=1.0, height=2.0, slices=40, stacks=40):
    super().__init__()
    self.materia = materia
    self.quadric = ZOpenGLQuadric();
    if self.materia == None:
      self.materia = ZOpenGLMateria()
      
    texture= self.gettexture()
    
    self.quadric.texture(texture);
      
    self.cylinder = ZOpenGLCylinder(self.quadric, self.materia)
    self.cylinder.reshape(base, top, height, slices, stacks)

    self.load(filename);
    self.drawStyle(GLU_FILL);
 

  def drawStyle(self, style):
    #style will take GLU_FILL, GLU_LINE, GLU_SILHOUETTE, and GLU_POINT. 
    self.quadric.drawStyle(style);    
  
  def orientation(self, orientation):
    #orientation will take GLU_OUTSIDE, and GLU_INSIDE
    self.quadric.orientation(orientation);

 
  def normals(self, normal):
    #normal will take GLU_NONE, GLU_FLAT, and GLU_SMOOTH
    self.quadric.normals(normal);
 

  def load(self, filename):
    self.bind();

    self.pixelStore(GL_UNPACK_ALIGNMENT, 4);
    
    self.parameter(GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    self.parameter(GL_TEXTURE_MIN_FILTER, GL_NEAREST);

    self.parameter(GL_TEXTURE_WRAP_S, GL_REPEAT);
    self.parameter(GL_TEXTURE_WRAP_T, GL_REPEAT);
    self.env(GL_TEXTURE_ENV_MODE, GL_MODULATE)

    self.imageFromFile(filename);
    self.unbind();
 


  def draw(self):  
    self.bind();
    self.cylinder.draw();
    self.unbind()
