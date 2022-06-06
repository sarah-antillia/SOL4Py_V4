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

#  ZOpenGLMainView.py

# encodig: utf-8

import sys
import os
import math
import traceback

import numpy as np

from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtOpenGL     import *

import OpenGL
#import OpenGL.GL as gl

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image, ImageOps

from SOL4Py.ZApplicationView import *
from SOL4Py.ZScalableScrolledImageView  import *
from SOL4Py.ZVerticalPane    import * 
from SOL4Py.opengl.ZOpenGLView   import * 
 
class ZOpenGLMainView(ZApplicationView):
  
  # ZOpenGLMainView Constructor
  def __init__(self, title, x, y, width, height):
    super(ZOpenGLMainView, self).__init__(title, x, y, width, height)

  def help_about(self):
    QMessageBox.about(self, "About", "OpenGLApplication: Copyright (c) 2019 Antillia.com")
    

  def help_version(self):
    info = """
            Vendor:         {0}
            Renderer:       {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            glGetString(GL_VENDOR),
            glGetString(GL_RENDERER),
            glGetString(GL_VERSION),
            glGetString(GL_SHADING_LANGUAGE_VERSION)
        )
    QMessageBox.information(self, "Version", "SOL4Py1.0 on Python3 and PyQt5 " + info)
    
