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

#  ZOpenGLProgram.py

# encoding: utf-8

import sys
import os
import traceback

import numpy as np
import math

from SOL4Py.opengl.ZOpenGLObject import *

  
class ZOpenGLProgram(ZOpenGLObject): 

#ifdef GL_VERSION_2_0

  ## Constructor
  def __init__(self):
    super().__init__()
    self.program = self.create()
    if self. program == 0: 
      raise ValueError("Failed to glCreateProgram.")

  
  def attachShader(self, shader):
    glAttachShader(self.program, shader.shader)
  
  
  def bindAttributeLocation(self, index, name):
    glBindAttribLocation(self.program, index, name)


  def create(self):
    return glCreateProgram()


  def delete(self):
    glDeleteProgram(self.program)


  def detachShader(self, shader):
    glDetachShader(self.program, shader.shader)


  def getActiveAttribute(self, index):
    # length, size, type, name will be returned.
    return glGetActiveAttrib(self.program, index)
    
  
  def getAttachedShaders(self, maxCount):
    # count, shaders will be returned
    return glGetAttachedShaders(self.program, maxCount)


  def getAttributeLocation(self, name):
    return glGetAttribLocation(self.program, name)


  def getProgramInfoLog(self):
    # infoLog will be returned.
    return glGetProgramInfoLog(self.program)


  def getProgram(self):
    return self.program


  def getProgramiv(self, pname):
    return glGetProgramiv(self.program, pname)


  def getActiveAttributes(self):
    return self.getProgramiv( GL_ACTIVE_ATTRIBUTES)


  def getActiveAttributeMaxLength(self):
    return self.getProgramiv(GL_ACTIVE_ATTRIBUTE_MAX_LENGTH)
  

  def getActiveUniforms(self):
    return self.getProgramiv(ACTIVE_UNIFORMS)
  

  def getActiveUniformMaxLength(self):
    return self.getProgramiv(GL_ACTIVE_UNIFORM_MAX_LENGTH)
  

  def getAttachedShaders(self):
    return self.getProgramiv(GL_ATTACHED_SHADERS)


  def getDeleteStatus(self):
    return self.getProgramiv(GL_DELETE_STATUS)


  def getLinkStatus(self):
    return self.getProgramiv(GL_LINK_STATUS)


  def getValidateStatus(self):
    return self.getProgramiv(GL_VALIDATE_STATUS)


  def getUniformLocation(self):
    # This will return name of location.
    return glGetUniformLocation(self.program)
  
  
  def getUniform(self, location):
    # This will return params list
    return glGetUniformfv(self.program, location)
  


  def isProgram(self):
    return glIsProgram(self.program)


  def link(self):
    glLinkProgram(self.program)
    
    linked = self.getProgramiv(GL_LINK_STATUS)
    if linked == GL_FALSE: 
      raise ValueError(self, "Failed to link.")


  def use(self):
    glUseProgram(self.program)


  def unuse(self):
    glUseProgram(0)


  def validate(self):
    glValidateProgram(self.program)


#ifdef GL_VERSION_3_0
    
  def getUniform(self, ocation):
    # This will return params
    return glGetUniformuiv(self.program, location)
  
#endif

  



