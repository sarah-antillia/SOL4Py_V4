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

# 2019/07/05

# Torch version

#  TorchInceptionV3Classifier.py

# See: https://pytorch.org/docs/master/torchvision/models.html#classification

# 
# encodig: utf-8

import sys
import os
import time
import traceback

sys.path.append('../../')

from SOL4Py.ZTorchImageClassifierView import *


DATASET_INCEPTIONV3 = 0

############################################################
# Classifier View

class MainView(ZTorchImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
            datasets = {"InceptionV3": DATASET_INCEPTIONV3})
    #  Load trained model
    self.write("Loading InceptionV3 model")
    
    self.model = models.inception_v3(pretrained=True)
    #  Change the self.model to aneval mode 
    self.model.eval()
    
    self.load_class_names()

    self.model_loaded = True
    
    self.write("Loaded InceptionV3 model")
    self.show()


  def load_class_names(self):
    class_index_file = './imagenet_class_index.json'
    self.write("load class index file {}".format(class_index_file))
    
    with open(class_index_file, 'r') as indexfile:
      class_index = json.load(indexfile)
      self.classes = {int(key):value[1] for (key, value) in class_index.items()}



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
    
