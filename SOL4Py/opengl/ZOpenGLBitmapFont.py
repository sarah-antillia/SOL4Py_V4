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

#  ZOpenGLBitmapFont.py

# encodig: utf-8

import sys

# 

from SOL4Py.opengl.ZOpenGLObject import *


class ZOpenGLBitmapFont(ZOpenGLObject):
  ## Construcotr
  
  def __init__(self, font = GLUT_BITMAP_TIMES_ROMAN_24):
    if self.isBitmapFont(font):
      self.font = font
    else:
      raise ValueError("Invalid font name")

  
  def draw(self, x, y, z, text):
    if text == None:
      return

    self.text = text
  
    size = len(self.text)
    glPushMatrix()
    glRasterPos3f(x, y,z)
    for i in range(size):
      glutBitmapCharacter(self.font, ord(self.text[i]))
    glPopMatrix()


  def isBitmapFont(self, font):
    fonts = [
       GLUT_BITMAP_9_BY_15,
       GLUT_BITMAP_8_BY_13,
       GLUT_BITMAP_TIMES_ROMAN_10,
       GLUT_BITMAP_TIMES_ROMAN_24,
       GLUT_BITMAP_HELVETICA_10,
       GLUT_BITMAP_HELVETICA_12,
       GLUT_BITMAP_HELVETICA_18,
     ]
    rc = False
    for i in range(len(fonts)):
      if  font == fonts[i]:
        rc = True
        break
    return rc

