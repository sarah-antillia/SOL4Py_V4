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

#  ZColor4.py

# encodig: utf-8

 
class ZColor4:

  # ZColor4 Constructor
  def __init__(self, r, g, b, a):
    self.set(r, g, b, a)
    
  def set(self, r, g, b, a):
    self.r = r
    self.g = g
    self.b = b
    self.a = a
    

