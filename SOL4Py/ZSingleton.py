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

#  ZSingleton.py

# encoding utf-8

import sys
import os
import traceback

class ZSingleton:
  # class variable
  _singleton = None
  
  def set_instance(instance):
    if ZSingleton._singleton == None:
      ZSingleton._singleton = instance
    else:
      raise Exception("Already registered an instaance".format(ZSingleton._singleton))
   
  def get_instance():
    return ZSingleton._singleton
    
