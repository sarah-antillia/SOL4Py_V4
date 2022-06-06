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

#  ZOpenGLImage.py

# encodig: utf-8

import numpy as np

from PIL import Image, ImageOps
 
class ZOpenGLImage:
  
  # ZOpenGLImage Constructor
  def __init__(self, filename, flip=True):
    image = Image.open(filename)
    if flip == True:
      image = ImageOps.flip(image)
      
    self.width, self.height = image.size
    try:
      image = image.convert("RGBA")
      self.bytes = image.tobytes("raw", "RGBA", 0, -1)
    except SystemError:
      self.bytes = image.tobytes("raw", "RGBX", 0, -1)
