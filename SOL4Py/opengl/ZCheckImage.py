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

#  ZCheckImage.py

# encodig: utf-8

import math
import numpy as np

class ZCheckImage:
  WIDTH  = 8
  HEIGHT = 8

  ##
  # Constructor
  
  def __init__(self):
  
    # Create a texture from a RGBA checker board image of size WIDHT and HEIGHT 
    data= np.zeros(self.WIDTH * self.HEIGHT * 4, dtype=np.byte).reshape((self.WIDTH, self.HEIGHT, 4))

    for i in range(self. HEIGHT):
      for j in range(self.WIDTH):
        if (i + j) % 2 == 0: 
          c = 255  
          # white
          data[i][j][0] = np.byte(c)
          data[i][j][1] = np.byte(c)
          data[i][j][2] = np.byte(c)
        else:
          c= 255 
          # red
          data[i][j][0] = np.byte(c)   
          data[i][j][1] = 0 
          data[i][j][2] = 0 
 
        data[i][j][3] = 0 
        
    self.data = data
    

