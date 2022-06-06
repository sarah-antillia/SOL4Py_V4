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

# VegeFruitsDataSetAugmentor.py

# 2019/04/22

# encodig: utf-8

import sys
import os
import time
import traceback
#import keras
 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.keras.ZDataSetAugmentor import *
from SOL4Py.keras.ZDataSetLoader import *


############################################################
#  

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
       
    augmentation = 100
    
    if len(sys.argv) ==2:
      augmentation = int(sys.argv[1])
 
    
    mini_dataset       = ("./mini_dataset",      "jpg")
    augmented_dataset  = ("./augmented_dataset", "png")

    print("augmentation:      " + str(augmentation))
    print("mini_dataset:      " + str(mini_dataset))
    print("augmented_dataset: " + str(augmented_dataset))
       
    # 1 Generate augmented images from mini_dataset,  and save them to augmented_dataset.
    augmentor = ZDataSetAugmentor()
    augmentor.generate(mini_dataset, augmented_dataset, n_augmentation=augmentation)
    
 
    # 2 Load the augmented_dataset
    loader    = ZDataSetLoader()
    loader.load_dataset(augmented_dataset)
    
    loader.show_summary()
    
  except:
    traceback.print_exc()


