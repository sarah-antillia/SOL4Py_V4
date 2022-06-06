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

#  ZTextureCoordTriangularBox.py

# encodig: utf-8

import numpy as np
import math
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *


class ZTextureCoordTriangularBox(ZOpenGLObject):
  
  def __init__(self, x=1.0, y=1.0, z=1.0):
    super().__init__()
  
    #TextureCoord2Vertex3
    self.box  = [
        # Front
        # Face 0-1-2
        [[1.0, 1.0], [  x,  y, z]],
        [[0.0, 1.0], [ -x,  y, z]],
        [[0.0, 0.0], [ -x, -y, z]],
        # Face 2-3-0
        [[0.0, 0.0], [ -x, -y, z]],
        [[1.0, 0.0], [  x, -y, z]],
        [[1.0, 1.0], [  x,  y, z]],

        # Right
        # Face 0-3-4
        [[0.0, 1.0], [  x,  y,  z]],
        [[0.0, 0.0], [  x, -y,  z]],
        [[1.0, 0.0], [  x, -y, -z]],
        # Face 4-5-0
        [[1.0, 0.0], [  x, -y, -z]],
        [[1.0, 1.0], [  x,  y, -z]],
        [[0.0, 1.0], [  x,  y,  z]],

        # Top 
        # Face 0-5-6
        [[1.0, 0.0], [  x,  y,  z]],
        [[1.0, 1.0], [  x,  y, -z]],
        [[0.0, 1.0], [ -x,  y, -z]],
        # Face 6-1-0
        [[0.0, 1.0], [ -x,  y, -z]],
        [[0.0, 0.0], [ -x,  y,  z]],
        [[1.0, 0.0], [  x,  y,  z]],

        # Left
        # Face  1-6-7
        [[1.0, 1.0], [ -x,  y,  z]],
        [[0.0, 1.0], [ -x,  y, -z]],
        [[0.0, 0.0], [ -x, -y, -z]],
        # Face 7-2-1
        [[0.0, 0.0], [ -x, -y, -z]],
        [[1.0, 0.0], [ -x, -y,  z]],
        [[1.0, 1.0], [ -x,  y,  z]],

        # Bottom 
        # Face 7-4-3
        [[0.0, 0.0], [ -x, -y, -z]],
        [[1.0, 0.0], [  x, -y, -z]],
        [[1.0, 1.0], [  x, -y,  z]],
        # Face 3-2-7
        [[1.0, 1.0], [  x, -y,  z]],
        [[0.0, 1.0], [ -x, -y,  z]],
        [[0.0, 0.0], [ -x, -y, -z]],

        # Back
        # Face 4-7-6
        [[0.0, 0.0], [  x, -y, -z]],
        [[1.0, 0.0], [ -x, -y, -z]],
        [[1.0, 1.0], [ -x,  y, -z]],
        # Face 6-5-4
        [[1.0, 1.0], [ -x,  y, -z]],
        [[0.0, 1.0], [  x,  y, -z]],
        [[0.0, 0.0], [  x, -y, -z]]
    ]
    
    self.n_elements = len(self.box)
    self.n_faces    = 6
    self.n_vertices_per_face = 6


  def getBox(self):
    return self.box


  def getNumberOfElements(self):
    return self.n_elements


  def getNumberOfFaces(self):
    return self.n_faces
  
  
  def getNumberOfVerticesPerFace(self):
    return self.n_vertices_per_face
       
       