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

#  ZColoredCheckImage.py

# encodig: utf-8

import math
import numpy as np

class ZColoredCheckImage:
  WIDTH  = 64
  HEIGHT = 64

  ##
  # Constructor
  
  def __init__(self, r=True, g=True, b=True):
  
    # Create a texture from a RGBA black and white checker board image of size WIDHT and HEIGHT 
    data= np.zeros(self.WIDTH * self.HEIGHT * 4, dtype=np.byte).reshape((self.WIDTH, self.HEIGHT, 4))

    for i in range(self. HEIGHT):
      for j in range(self.WIDTH):
        c = (((i & 0x8) == 0) ^ ((j & 0x8) == 0)) * 255;
        if r == True:
          data[i][j][0] = np.byte(c)
        else:
          data[i][j][0] = np.byte(255)
        if g == True:
          data[i][j][1] = np.byte(c)
        else:
          data[i][j][1] = np.byte(255)
          
        if b == True:
          data[i][j][2] = np.byte(c)
        else:
          data[i][j][2] = np.byte(255)
          
        data[i][j][3] = np.byte(255)
      
    self.data = data
    

