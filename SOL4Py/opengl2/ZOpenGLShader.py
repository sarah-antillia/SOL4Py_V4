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

#  ZOpenGLShader.py

# encoding: utf-8

import sys
import os
import traceback

import math
#import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *

#ifdef GL_VERSION_2_0


class ZOpenGLShader(ZOpenGLObject):
  
  ## This constructor will simply create a shader object.
  # You shoud call load_file or load_string to load and compile 
  #a source for the shader. 
  
  def __init__(self,  type):
    self.type = type
    super().__init__()
    self.shader = self.INVALID_VALUE
    # 1 Create shader
    self.shader = self.create(type)
    if self.shader == 0: 
      raise ValueError("Failed to createShader: " + str(type)) 
    
      
  def load_file(self, filename):
    # 1 Read source from a file
    self.fullpath = os.path.abspath(filename)
    print(self.fullpath)
    
    #with open(self.fullpath, "r", "utf-8") as shader_file:
    with open(self.fullpath, "r") as shader_file:
      source = shader_file.read()
       
      # 2 Set the source to the self.shader 
      self.setShaderSource(source)
    
    # 3 Compile
    self.compile()


  def load_string(self, source):
    # 1 Set the source to the self.shader 
    self.setShaderSource(source)
    
    # 2 Compile
    self.compile()


  def create(self, type):
    return glCreateShader(type)

  
  def setShaderSource(self, string):
    glShaderSource(self.shader, string)


  def  compile(self):
    glCompileShader(self.shader)
    compiled = self.getShader(GL_COMPILE_STATUS)
    if compiled == GL_FALSE: 
      self.delete()
      error = self.getShaderInfoLog()
      raise RuntimeError("Failed to compile a shader " + self.fullpath + " Error: " + error)


  def delete(self):
    if self.shader > 0: 
      glDeleteShader(self.shader)
      
    self.shader = self.INVALID_VALUE


  def getShaderInfoLog(self, decoding="utf-8"):
    return glGetShaderInfoLog(self.shader).decode(decoding)


  def getShaderSource(self, decoding="utf-8"):
    return glGetShaderSource(self.shader).decode(decoding)


  """
  getShader:  pname takes one of the following values:
   GL_SHADER_TYPE,
   GL_DELETE_STATUS
   GL_COMPILE_STATUS
   GL_INFO_LOG_LENGTH
   GL_SHADER_SOURCE_LENGTH
  """
  
  def getShader(self, pname):
    # This will return value for param.
    return glGetShaderiv(self.shader, pname)
  

  def getShaderType(self):
    return self.getShader(GL_SHADER_TYPE)


  def getDeleteStatus(self):
    return getShader(GL_DELETE_STATUS)
  

  def getCompileStatus(self):
    return self.getShader(GL_COMPILE_STATUS)


  def getInfoLogLength(self):
    return self.getShader(GL_INFO_LOG_LENGTH)


  def getShaderSourceLength(self):
    return self.getShader(GL_SHADER_SOURCE_LENGTH)


  def isShader(self):
    return glIsShader(self.shader)



#endif

