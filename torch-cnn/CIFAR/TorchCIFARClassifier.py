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

# 2019/06/30
# 2019/09/18

# On CIFAR-10 dataset, see the following page:

# http://www.cs.toronto.edu/~kriz/cifar.html

# See: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html#loading-and-normalizing-cifar10
#
#  TorchCIFARClassifier.py

# encodig: utf-8

import sys
import os
import time
import traceback
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np


sys.path.append('../../')

from SOL4Py.ZTorchImageClassifierView import *
from SOL4Py.torch.ZTorchImagePreprocessor import ZTorchImagePreprocessor

from TorchCIFARModel import *

CIFAR10  = 0
CIFAR100 = 1

############################################################
# Classifier View

class MainView(ZTorchImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                        datasets = {"CIFAR10": CIFAR10, "CIFAR100": CIFAR100})
                            
    self.model_loaded = False
    
    self.class_names_set = [None, None]
    
    self.resize = 32
    self.crop   = 32
    self.image       = None
                        
    # The names of the classes.
    # See https://github.com/ageron/tensorflow-models/blob/master/slim/datasets/download_and_convert_cifar.py
    
    self.class_names_set[CIFAR10] = [ 
                'airplane','automobile', 'bird',     'cat',    'deer',
                'dog',     'frog',       'horse',    'ship',   'truck',]

    self.class_names_set[CIFAR100] = [
                'apple',      'aquarium_fish', 'baby',       'bear',         'beaver',
                'bed',        'bee',           'beetle',     'bicycle',      'bottle',
                'bowl',       'boy',           'bridge',     'bus',          'butterfly',
                'camel',      'can',           'castle',     'caterpillar',  'cattle',
                'chair',      'chimpanzee',    'clock',      'cloud',        'cockroach',
                'couch',      'crab',          'crocodile',  'cup',          'dinosaur',
                'dolphin',    'elephant',      'flatfish',   'forest',       'fox',
                'girl',       'hamster',       'house',      'kangaroo',     'keyboard',
                'lamp',       'lawn_mower',    'leopard',    'lion',         'lizard',
                'lobster',    'man',           'maple_tree', 'motorcycle',   'mountain',
                'mouse',      'mushroom',      'oak_tree',   'orange',       'orchid',
                'otter',      'palm_tree',     'pear',       'pickup_truck', 'pine_tree',
                'plain',      'plate',         'poppy',      'porcupine',    'possum',
                'rabbit',     'raccoon',       'ray',        'road',         'rocket',
                'rose',       'sea',           'seal',       'shark',        'shrew',
                'skunk',      'skyscraper',    'snail',      'snake',        'spider',
                'squirrel',   'streetcar',     'sunflower',  'sweet_pepper', 'table',
                'tank',       'telephone',     'television', 'tiger',        'tractor',
                'train',      'trout',         'tulip',      'turtle',       'wardrobe',
                'whale',      'willow_tree',   'wolf',       'woman',        'worm',]

    
    #  Load trained model
    
    self.model = TorchCIFARModel(self.dataset_id, mainv=self)
    
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create()
      self.model.load()    # Load a trained weight
      self.model.evaluate()
      self.model_loaded = True
    else:
      print("You have to create a model file")
      print("Please run: python CIFARModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "MNIST", 
           "Mode file is missing.\nPlease run: python CIFARModel.py " + str(self.dataset_id))

    self.show()



  def datasets_activated(self, text):
    self.dataset_id = self.datasets[text]
    title = self.get_title()
    self.setWindowTitle(text + " - " + title)

    self.classifier_button.setEnabled(False)
    
    self.model.set_dataset_id(self.dataset_id)
    self.model.load_dataset()
    
    if self.model.is_trained():
    
      self.model.load()
      #self.model.evaluate()
      self.model_loaded = True
      
    else:
      self.model.build()
      
      print("You have to create a model file and weight file")
      print("Run: python TorchCIFARModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "CIFAR", 
           "Model/Weight File Missing.\nPlease run: python TorchCIFARModel.py " + str(self.dataset_id))
 

  def classify(self):
    self.write("--------------------------------------------")
    self.write("classify start.")
    self.write(self.filename)
    input = Variable(self.image_tensor)
    index = self.model.predict(input)
    classes = self.class_names_set[self.dataset_id]
    label   = classes[index]
    self.write("Prediction: {}".format(label) )

    self.write("classify end.")


############################################################
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 900, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()
    
