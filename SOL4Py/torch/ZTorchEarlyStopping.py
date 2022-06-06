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
from SOL4Py.torch.ZTorchCallback    import *


class ZTorchEarlyStopping(ZTorchCallback):
  ##
  # Constructor
  def __init__(self, monitor="val_loss", mode="min"):
    super(ZTorchEpochChangeNotifier, self).__init__()
    self.monitor  = monitor
    self.mode     = mode
    
    self.acc      = 0.0
    self.loss     = 0.0
    self.val_acc  = 0.0
    self.val_loss = 0.0
    pass


  def on_epoch_end(self, epoch, logs):
    rc = False
    if "," in logs:
      epoch, loss, acc, val_loss, val_acc = log.split(",")
      print("{} {} {} {}".format(loss, acc, val_loss, val_acc))
      prev_acc      = self.acc
      prev_loss     = self.loss
      prev_val_acc  = self.val_acc
      prev_val_loss = self.val_loss
      
      self.acc      = float(acc)
      self.loss     = float(loss)
      self.val_acc  = float(val_acc)
      self.val_loss = float(val_loss)
      # TO DO 
      # implementation
    
    return rc


