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

#2016/09/10 On calculateSurfaceNormals method, see: https://www.opengl.org/wiki/Calculating_a_Surface_Normal
 
#  ZOpenGLQuadSurfaces.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLQuadSurfaces:

  ## Constructor
  def __init__(self, vertices, faces):
    self.vertices   = vertices   # list of vertex = [x, y, z]
    self.n_vertices = len(self.vertices)
    self.faces      = faces
    self.n_faces   = len(self.faces)
    self.normals    = None
    self.n_normals  = 0


  def calculateSurfaceNormals(self):

    self.n_normals = self.n_faces;
    self.STRIDE  = 3
    
    self.normals = [[0.0 for i in range(0, self.STRIDE)] for j in range(0, self.n_faces)]
    
    for s in range(self.n_faces):
      quad = self.faces[s];

      v = [
        self.vertices[ quad[0] ],
        self.vertices[ quad[1] ],
        self.vertices[ quad[2] ],
        self.vertices[ quad[3] ]
      ]
      
      normal = [0, 0, 0]
      
      for i  in range(self.STRIDE+1):
        j = (i+1) % (self.STRIDE+1);
        normal[0] += (v[i][1] - v[j][1]) * (v[i][2] + v[j][2]);
        normal[1] += (v[i][2] - v[j][2]) * (v[i][0] + v[j][0]);
        normal[2] += (v[i][0] - v[j][0]) * (v[i][1] + v[j][1]);
      
      normal = self.normalize(normal);
        
      self.normals[s][0] = normal[0];
      self.normals[s][1] = normal[1];
      self.normals[s][2] = normal[2];
   
    self.n_normals = len(self.normals)
    return self.normals
    

  def normalize(self, v):
    sq = 0
    for i in range(len(v)):
      sq += v[i]*v[i]
    length = math.sqrt(sq)
    
    for i in range(len(v)):
      v[i] = v[i] /length
    
    return v

    