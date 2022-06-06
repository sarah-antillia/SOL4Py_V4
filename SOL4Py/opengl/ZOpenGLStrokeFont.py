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

#  ZOpenGLStrokeFont.py

# encodig: utf-8

import sys

# 

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLStrokeFont(ZOpenGLObject):
  ## Constructor
  
  def __init__(self, font = GLUT_STROKE_ROMAN):
    if self.isStrokeFont(font):
      self.font = font
    else:
      raise ValueError("Invalid font")
      

  def draw(self, x, y, z, text, scale=0.2):
    if text == None:
      return
    else:
      self.text = text
            
    size = len(self.text)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, -1.0*scale, scale)
    for i in range(size):
      glutStrokeCharacter(self.font, ord(self.text[i]))
    glPopMatrix()
  
  
  def isStrokeFont(self, font):
    fonts = [
       GLUT_STROKE_ROMAN,
       GLUT_STROKE_MONO_ROMAN,
     ]
    rc = False
    for i in range(len(fonts)):
      if  font == fonts[i]:
        rc = True
        break
    return rc


