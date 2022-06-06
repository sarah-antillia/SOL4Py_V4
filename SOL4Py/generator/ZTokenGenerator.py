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

# 2020/01/20
# ZTokenGenerator.py

# encoding: utf-8

import os

class ZTokenGenerator:
   DEFAULT_LENGTH = 16
   
   def __init__(self):
     pass
  
   #Generate a random bytes array of hex format with specified byte size.
   def generate(self, size):
       if size <self.DEFAULT_LENGTH:
           size = self.DEFAULT_LENGTH
           
       return os.urandom(size).hex()
           
   # Usage
   # generator = ZTokenGenerator()
   # twentybytes_random_token = generator(20)
   # which may not be a real unique token, but it may be much better than ordinary uuid4 of 16bytes.   
