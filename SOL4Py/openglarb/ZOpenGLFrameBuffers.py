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

#  ZOpenGLFrameBuffers.py

# encodig: utf-8
import numpy as np
import OpenGL

from SOL4Py.opengl.ZOpenGLObject import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.GL.EXT.framebuffer_object import *

#ifdef GL_ARB_framebuffer_object

class ZOpenGLFrameBuffers(ZOpenGLObject):

 
  ## Constructor
  def __init__(self, size, target):
    super().__init__()
 
    self.size   = size
    self.target = target
    self.buffer = None
    
    if size <= 0:
      raise ValueError("Invalid size parameter. size" + str(size)) ;
      
    self.buffer = glGenFramebuffers(self.size);


  def unbind(self):
    glBindFramebuffer(self.target, 0);

  def delete(self):
    glDeleteFramebuffers(self.size, self.buffers);  
  
  def blit(self, srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, 
                dstX1, dstY1, mask, filter):
    
    glBlitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, 
           dstX1, dstY1, mask, filter);
  
  def check(self):
    return glCheckFramebufferStatus(self.target);


  def attachRenderbuffer(self, attachment, renderbuffertarget, renderbuffer):
    glFramebufferRenderbuffer(self.target, attachment, renderbuffertarget, renderbuffer);


  def detachRenderbuffer(self,attachment, renderbuffertarget):
    attachRenderbuffer(self.target, attachment, renderbuffertarget, 0);


  def texture1D(self, attachment, textarget, texture, level):
    glFramebufferTexture1D(self.target, attachment, textarget, texture, level);


  def texture2D(self, attachment, textarget, texture, level):
    glFramebufferTexture2D(self.target, attachment, textarget, texture, level);


  def texture3D(self, attachment, textarget, texture, level, zoffset):
    glFramebufferTexture3D(self.target, attachment, textarget, texture,level, zoffset);


  def getAttachmentParameteriv(self, attachment, pname):
    return glGetFramebufferAttachmentParameteriv(self.target, attachment, pname)


  def isFramebuffer(self):
    return glIsFramebuffer(self.buffer);


  def get(self, n=0):
    if self.size == 1:
      return self.buffers
  
    if n > 0 and n < self.size:
      return self.buffers[n];
    else:
      raise ValueError("Invalid index " + str(n));


  def bind(self, n=0):
    if self.size == 1:
      glBindFramebuffer(self.target, self.buffer);
    elif n > 0 and n < self.size:
      glBindFramebuffer(self.target, self.buffer[n]);
    else:
      raise ValueError("Invalid index " + str(n)) ;


#endif
  
  