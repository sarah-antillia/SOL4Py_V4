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

# 2019/09/10


#  TorchMNISTClassifier.py

# encodig: utf-8

import sys
import os
import time
import traceback

import numpy as np
from PIL import Image

sys.path.append('../../')

from SOL4Py.torch.ZTorchImagePreprocessor import ZTorchImagePreprocessor
from SOL4Py.ZTorchImageClassifierView import *

from TorchMNISTModel import TorchMNISTModel

MNIST         = 0
FASHION_MNIST = 1


############################################################
# Classifier View

class MainView(ZTorchImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                  datasets = {"MNIST": MNIST, "FashionMNIST": FASHION_MNIST})
 
    self.class_names_set = [None, None]
    self.resize = 28
    self.crop   = 28    
    # ndarry image datat created from keras.preprocessing.image
    self.image       = None
                            
    self.class_names_set[MNIST] = ["0", "1", "2", "3", "4",
                                   "5", "6", "7", "8", "9"]
    self.class_names_set[FASHION_MNIST]  =['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    self.image        = None
    self.model_loaded = False
  
    # Load trained model
    
    self.model = TorchMNISTModel(self.dataset_id, epochs = 10, mainv=self)
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create()
      self.model.load()    # Load a trained weight
      #self.model.evaluate()
      self.model_loaded = True
      
    else:
      print("You have to create a model file.")
      print("Run: python TorchMNISTModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "MNIST", 
           "Model/Weight File Missing.\nPlease run: python TorchMNISTModel.py " + str(self.dataset_id))
  
    self.show()


  def datasets_activated(self, text):
    self.dataset_id = self.datasets[text]
    title = self.get_title()
    self.setWindowTitle(text + " - " + title)
    self.model.set_dataset_id(self.dataset_id)
      
    self.classifier_button.setEnabled(False)
    
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.load()
      #self.model.evaluate()
      self.model_loaded =True        
      QMessageBox.information(self, "TorchMNIST", 
           "OK: TorchMNIST Model files loaded")

    else:
      print("You have to create a model file and a weight file.")
      print("Please run: python TorchMNISTModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "MNIST", 
           "Model/Weight files missing.\nPlease run: python TorchMNISTModel.py " + str(self.dataset_id))


  def load_filexx(self, filename):
    self.ndarray = None
    resize = 28
    crop   = 28
    try:      
      # 1 Open an original image file by PIL Image class.
      self.image = Image.open(filename)
      # You have to convert the self.image to a gray scale image
      self.image = self.image.convert("L")
      
      self.image_view.set_image(np.array(self.image)) 
      self.resized_image = self.image.resize((resize, resize))

      preprocessor = ZTorchImagePreprocessor()
  
      self.set_filenamed_title(filename)
      
      # 2 Crop the image.  
      self.cropped_image = preprocessor.image_crop(self.image, resize, crop)
      
      # 3 Convert the self.image to numpy ndarray. 
      self.ndarray  = np.array(self.cropped_image)

      # 4 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.ndarray)

    except:
      self.write(formatted_traceback())

  def load_file(self, filename):
    self.ndarray = None
    try:      
      # 1 Open an original image file by PIL Image class.
      self.image = Image.open(filename)
      # You have to convert the self.image to a gray scale image
      self.image = self.image.convert("L")
      
      self.image_view.set_image(np.array(self.image)) 
      self.resized_image = self.image.resize((self.resize, self.resize))

      preprocessor = ZTorchImagePreprocessor()
  
      self.set_filenamed_title(filename)
      
      # 2 Crop the image.  
      self.cropped_image = preprocessor.image_crop(self.image, self.resize, self.crop)
      
      # 3 Convert the self.image to numpy ndarray. 
      self.ndarray  = np.array(self.cropped_image)

      # 4 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.ndarray)

    except:
      self.write(formatted_traceback())


  def classify(self):
    self.write("--------------------------------------------")
    self.write("classify start")
    self.write(self.filename)

    index = self.model.predict(self.cropped_image)
    classes = self.class_names_set[self.dataset_id]
    label   = classes[index]
    self.write("Prediction: {}".format(label) )
         
    self.write("classify end")



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
    
