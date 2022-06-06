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
 
#  ZVector.py

# encodig: utf-8

class ZVector:

  def __init__(self, size):
    self.size = size
    if size < 1:
      raise ValueError("VectorF: invalid size")
     
    self.v = [0.0 for i in range(size)]


  def set(self,i, value):  
    if i<0 or i >=self.size:
      raise ValueError("VectorF: invalid index")
    self.v[i] = value


  def get(self,i):  
    if i<0 or i >=self.size:
      raise ValueError("VectorF: invalid index")
    return self.v[i]


  def put(self, list):
    if len(list) != self.size:
      raise ValueError("VectorF: invalid size")
    self.v = list


  def vector(self):
     return self.v


  def to_array(self):
    return np.array(self.vector, "float32")

