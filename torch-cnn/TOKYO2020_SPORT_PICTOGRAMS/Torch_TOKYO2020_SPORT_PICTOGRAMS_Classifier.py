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

# 2019/07/13

#  Torch_TOKYO2020_SPORT_PICTOGRAMS_Classifier.py

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

from SOL4Py.torch.ZTorchImagePreprocessor import ZTorchImagePreprocessor
from SOL4Py.ZTorchImageClassifierView import *

from Torch_TOKYO2020_SPORT_PICTOGRAMS_Model import *

TOKYO2020_SPORT_PICTOGRAMS = 0


############################################################
# Classifier View

class MainView(ZTorchImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
               datasets= {"TOKYO2020_SPORT_PICTOGRAMS": TOKYO2020_SPORT_PICTOGRAMS})

    self.model_loaded = False
        
    self.resize = 64 #128
    self.crop   = 64 #128

    self.image       = None
    #  Load trained model
    self.classes = self.get_class_names()

    self.model = Torch_TOKYO2020_SPORT_PICTOGRAMS_Model(self.dataset_id, mainv=self)
    
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create()
      self.model.load()    # Load a trained weight
      self.model.evaluate()
      self.model_loaded = True
    else:
      print("You have to create a model file")
      print("Please run: python TOKYO2020_SPORT_PICTOGRAMS_Model.py " + str(self.dataset_id))
      QMessageBox.warning(self, "Torch_TOKYO2020_SPORT_PICTOGRAMS_Classifier", 
           "Mode file is missing.\nPlease run: python Torch_TOKYO2020_SPORT_PICTOGRAMS_Model.py " + str(self.dataset_id))

    self.show()


  def classify(self):
    self.write("--------------------------------------------")
    self.write("classify start.")
    self.write(self.filename)
    index = self.model.predict(self.cropped_image)

    label   = self.classes[index]
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
    
