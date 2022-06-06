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

# 2019/07/10

# ZTorchModelCheckPoint.py

# encodig: utf-8

import os
import sys

import traceback

sys.path.append('../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZMain    import *
from SOL4Py.torch.ZTorchCallback    import *


class ZTorchModelCheckPoint(ZTorchCallback):
  ##
  # Constructor
  def __init__(self, dataset_id=0, save_starting_val_loss=0.3, 
                 save_fileformat="{id:02d}-{epoch:02d}-{train_loss:.2f}-{val_loss:.2f}.pt"):
    super(ZTorchModelCheckPoint, self).__init__()
    self.dataset_id = id
    self.monitor  = "val_loss"
    self.save_starting_val_loss = save_starting_val_loss
    self.save_filefomrat        = save_fileformat
    self.acc      = 0.0
    self.loss     = 0.0
    self.val_acc  = 0.0
    self.val_loss = 0.0
    pass


  def on_epoch_end(self, epoch, logs):
    if "," in logs:
      epoch, loss, acc, val_loss, val_acc = log.split(",")
      print("{} {} {} {}".format(loss, acc, val_loss, val_acc))
      self.acc      = float(acc)
      self.loss     = float(loss)
      self.val_acc  = float(val_acc)
      self.val_loss = float(val_loss)
      if self.val_loss < self.save_starting_val_loss:
         filename = self.save_fileformat.fomrat(self.dataset_id, epoch, self.loss, self.val_loss)
         print("Save file {}".format(filename))
         torch.save(net.state_dict(), save_filename)
         
   

