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

# 2019/07/23 

#  TorchVegeFruitsDataset.py

# See: https://github.com/pytorch/tutorials/issues/78

import os
import glob

from random import *
import numpy as np

from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader
import torchvision.transforms

from scipy.io import loadmat
from PIL import Image

class TorchVegeFruitsDataset(Dataset):

  #TRAIN_DATA_DIR = "./dataset/train/"
  #VALID_DATA_DIR = "./dataset/valid/"


  ##
  # Constructor
  # 
  def __init__(self,  transform =None, root="./dataset/train/", image_file_extension = "jpg",):
      self.transform = transform
      self.images  = None
      self.root        = root
      self.image_folder = self.root + "/*/*." + image_file_extension
      
      files = glob.glob(self.image_folder)   # image_folder  = "./dataset/*/*.jpg"
      self.filenames_list = sorted(files)
      
      self.classes   = sorted( os.listdir(self.root) )
      self.nclasses = len(self.classes)
      print("NCLASSES {}".format(self.nclasses))
      

  def __getitem__(self, index):
      filename = self.filenames_list[index]
      image = Image.open(filename).convert('RGB')
      classname  = os.path.basename(os.path.dirname(filename))
      #print("category {}".format(classname))
      class_index = self.get_class_index(classname)
     
      if self.transform is not None:
         image = self.transform(image)
      return image, class_index


  def __len__(self):
    l = len(self.filenames_list)
    return l
    

  def get_class_index(self, classname):
    index = 0
    for i in range(len(self.classes)):
      if self.classes[i] == classname:
        index = i
        break
    return index
    
  