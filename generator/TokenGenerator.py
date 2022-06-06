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

# encoding: utf-8
# 2020/01/30

# TokenGenerator.py

import sys
import numpy as np

sys.path.append('../')
from SOL4Py.generator.ZTokenGenerator import *

###
#---------------------------------------------------------  

if __name__ == "__main__":
  generator = ZTokenGenerator()
  
  for i in range(20):
    name = generator.generate(20)
    print("{} Token: {}".format(i, name))
    
    