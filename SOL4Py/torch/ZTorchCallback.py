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

# 2019/06/25

# ZTorchCallback.py

# encodig: utf-8

import os
import sys

import traceback

sys.path.append('../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *

# This is a abstract ZTorchCallback class.

class ZTorchCallback:
  ##
  # Constructor
  def __init__(self):
    pass

  ## 
  # Destructor
  def __del__(self):
    print("ZTorchCallback.Destructor")


  def on_train_begin(self, logs={}):
    pass


  def on_epoch_end(self, epoch, logs):
    pass


