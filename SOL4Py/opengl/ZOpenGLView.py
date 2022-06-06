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

#  ZOpenGLView.py

# encodig: utf-8

import sys
import numpy as np

from PIL import Image, ImageOps

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtOpenGL     import *

import OpenGL

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# 
from SOL4Py.opengl.ZOpenGLObject import *
from SOL4Py.opengl.ZOpenGLBitmap import *


##--------------------------------------------
class ZOpenGLView(QOpenGLWidget):

  def __init__(self, parent=None):
    self.parent = parent
    super(QOpenGLWidget, self).__init__(parent)

  # Please define your own method in a subclass derived from this class.
  def minimumSizeHint(self):
    return QSize(50, 50)

  # Please define your own method in a subclass derived from this class.
  def sizeHint(self):
    return QSize(400, 400)

  # Please define your own method in a subclass derived from this class.
  def initializeGL(self):
    pass

  # Please define your own method in a subclass derived from this class.
  def paintGL(self):
    pass
      
  # Please define your own method in a subclass derived from this class.
  def resizeGL(self, width, height):
    side = min(width, height)
    if side < 0: 
      return
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(20.0, width / height, 0.5, 100.0)

    glMatrixMode(GL_MODELVIEW)


  def save(self, filename):
    x      = self.x()
    y      = self.y()
    width  = self.width()
    height = self.height()
    u_filename = filename.upper()
   
    if u_filename.endswith(".JPG"):
      bitmap = ZOpenGLBitmap(x, y, width, height, 24, GL_RGB)
      pixels = bitmap.readPixels(GL_FRONT)
      image  = Image.frombytes("RGB", (width, height), pixels)

    elif u_filename.endswith(".PNG"):     
      bitmap = ZOpenGLBitmap(x, y, width, height, 24, GL_RGBA)
      pixels = bitmap.readPixels(GL_FRONT)
      image = Image.frombytes("RGBA", (width, height), pixels)
    else:
      bitmap = ZOpenGLBitmap(x, y, width, height, 24, GL_RGB)
      pixels = bitmap.readPixels(GL_FRONT)
      image  = Image.frombytes("RGB", (width, height), pixels)
       
    image = ImageOps.flip(image)
    image.save(filename)

 