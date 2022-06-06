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

# 2019/05/19

#  download_weight_file.py

# If you would like to download the weight file "RoadSignsModel_0.h5"
# from antillia.com
# Please run this script file.


# encodig: utf-8

import sys
import os
import time
import traceback
import numpy as np
import zipfile
import tensorflow as tf

sys.path.append('../../')

from SOL4Py.ZMain import *


if main(__name__):
  try:
    weight_file = "RoadSignsModel_0.h5"

    if os.path.exists(weight_file) != True:

      zip_file = "RoadSignsModel_0.zip"
    
      url      = "http://www.antillia.com/sol4py/store/" + zip_file
      zip_file = tf.keras.utils.get_file(zip_file, url)
      print("You have downloaded {}".format(zip_file))

      with zipfile.ZipFile(zip_file) as zf:
        zf.extractall()
    else:
      print("OK, you have the weight file {}!".format(weight_file))
       
  except:
    traceback.print_exc()



