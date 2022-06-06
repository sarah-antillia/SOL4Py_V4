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

#  ZOpenGLList.py

# encodig: utf-8

from SOL4Py.opengl.ZOpenGLObject import *
#from SOL4Py.opengl.ZOpenGLMateria import *


class ZOpenGLList(ZOpenGLObject):

  def __init__(self, list=1, mode=GL_COMPILE ):
    super().__init__()
 
    if list <= 0:
      raise ValueError("Invalid list id:%d", list)
 
    if glIsList(list) == GL_TRUE:
      raise ValueError("Already used " + str(list))
 
    if mode == GL_COMPILE or mode == GL_COMPILE_AND_EXECUTE:
      glNewList(list, mode)
    else:
      raise ValueError("Invalid mode " + str(mode)) 

    self.list = list
    self.mode = mode

  def call(self):
    #if (mode == 0) {
      glCallList(list)
    #

