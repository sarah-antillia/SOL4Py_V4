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

#  ZOpenGLQuadric.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLQuadric(ZOpenGLObject):

  def __init__(self):
    super().__init__()
    self.quadric = gluNewQuadric()


  def delete(self):
    gluDeleteQuadric(self.quadric)


  def getQuadric(self):
    return self.quadric


  def orientation(self, orientation): #GLenum 
    #orientation will take GLU_OUTSIDE, and GLU_INSIDE
    gluQuadricOrientation(self.quadric, orientation)


  def texture(self, texture): #GLboolean
    gluQuadricTexture(self.quadric, texture)


  def drawStyle(self, style):  #GLenum 
    #style will take GLU_FILL, GLU_LINE, GLU_SILHOUETTE, and GLU_POINT. 
    gluQuadricDrawStyle(self.quadric, style)


  def normals(self, normal):  #GLenum 
    #normal will take GLU_NONE, GLU_FLAT, and GLU_SMOOTH
    gluQuadricNormals(self.quadric, normal)

