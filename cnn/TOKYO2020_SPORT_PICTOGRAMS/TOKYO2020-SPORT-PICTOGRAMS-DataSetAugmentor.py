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

# TOKYO2020-SPORT-PICTGRAMS-DataSetAugmentor.py

# 2019/05/13

# encodig: utf-8

import sys
import os
import time
import traceback
import keras
 
sys.path.append('../../')

from SOL4Py.ZMain import *
from SOL4Py.keras.ZDataSetAugmentor import *
from SOL4Py.keras.ZDataSetLoader import *


############################################################
#  

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
       
    augmentation = 10
    
    # To create images for training or validation, please specify 
    # target as "./dataset/train" or "./dataset/valid".
    target       = "./dataset/train"
    
    # To generate images for testing from ./mini_dataset".
    target       = "./test"

    if len(sys.argv) ==2:
      augmentation = int(sys.argv[1])
 
    if len(sys.argv) ==3:
      augmentation = int(sys.argv[1])
      target       = str(sys.argv[2])

    mini_dataset       = ("./mini_dataset",  "png")
    augmented_dataset  = (target,            "png")

    print("augmentation:      " + str(augmentation))
    print("mini_dataset:      " + str(mini_dataset))
    print("augmented_dataset: " + str(augmented_dataset))
       
    # 1 Generate augmented images from mini_dataset folder,  and save them to augmented_dataset folder.
    generator = ImageDataGenerator( 
                                        #rescale           = 1.0 /255, 
                                        rotation_range     = 20,
                                        width_shift_range  = 1.0,
                                        height_shift_range = 0.3,
                                        shear_range        = 0.4,
                                        zoom_range         = 0.3,
                                        brightness_range   = [0.7,1.2],
                                        channel_shift_range= 2.0,
                                        horizontal_flip    = False,  # We dont' flip pictograms images horizontally or vertically. 
                                        vertical_flip      = False)

    augmentor = ZDataSetAugmentor(generator)
    augmentor.generate(mini_dataset, augmented_dataset, n_augmentation=augmentation)
    
 
    # 2 Load the augmented_dataset
    loader    = ZDataSetLoader()
    loader.load_dataset(augmented_dataset)
    
    loader.show_summary()
    
  except:
    traceback.print_exc()


