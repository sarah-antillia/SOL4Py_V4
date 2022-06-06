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

# ZPasswordGenerator

# This is NOT using yield.
# encoding: utf-8

# See https://stackoverflow.com/questions/3854692/generate-password-in-python

import sys
import secrets
import numpy as np
import string
import random

sys.path.append('../')

from SOL4Py.generator.ZGenerator import ZGenerator


###
#---------------------------------------------------------  
class ZPasswordGenerator(ZGenerator):
  ##
  # Constructor
  def __init__(self):
    pass


  def generate(self, size=10):
    letters = string.printable.strip()
    password = ''
    
    for i in range(size):
      #It's much better to use secrets than random
      password += secrets.choice(letters)
      #password += random.choice(letters)
    return password 


if __name__ == "__main__":
  generator = ZPasswordGenerator()
  
  for i in range(20):
    name = generator.generate(12)
    print(name)

 
    