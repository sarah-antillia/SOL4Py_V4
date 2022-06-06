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

# 2019/04/22
# 2019/09/13 Updated load_file method not to use a temporary image file.

#  VegeFruitsClassifier.py

# This a simple VegeFruits ImageClassifier based on CIFAR-10 dataset, see the following page:

# http://www.cs.toronto.edu/~kriz/cifar.html

# See also:
# https://github.com/ageron/tensorflow-models/blob/master/slim/datasets/download_and_convert_cifar.py


# encodig: utf-8

import sys
import os
import time
import traceback

sys.path.append('../../')
from SOL4Py.ZImageClassifierView import *

from VegeFruitsModel import *

VEGEFRUITS_10  = 0

############################################################
# Classifier View

class MainView(ZImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                         datasets={"VegeFruits10": VEGEFRUITS_10})
    
    self.model_loaded = False
    self.image_size   = (VegeFruitsModel.WIDTH, VegeFruitsModel.HEIGHT)
    
    # keras.preprocessing.image
    self.image       = None

    #  Load trained model
    self.classes = self.get_class_names()

    self.model = VegeFruitsModel(self.dataset_id, mainv=self)
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create()
      self.model.load()
      self.model.compile()
      self.model.evaluate()
      self.model_loaded = True
    else:
      print("You have to create a model file and weight file")
      print("Please run: python VegeFruitsModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "VegeFruitsClassifier", 
           "Model/Weight File Missing.\nPlease run: python VegeFruitsModel.py " + str(self.dataset_id))

    self.show()



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
    
