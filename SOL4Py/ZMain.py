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

#  ZMain.py

import sys
import os
import traceback

def main(name):    
  if name == '__main__':
    return True
  else:
    return False

def formatted_traceback():
   return traceback.format_exc()


if main(__name__):
  try:
    node = Node()
    node.write()

  except Exception as ex:
     print("#Caught:Exception: {0}".format(ex))
  except:
    print("#Caught:" + formatted_traceback())
    
