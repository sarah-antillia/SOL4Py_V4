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

# 2019/05/29
# 2019/09/13 Updated load_file method not to use a temporary image file.

#  RoadSignslassifier.py

# encodig: utf-8

import sys
import os
import time
import traceback

sys.path.append('../../')

from SOL4Py.ZImageClassifierView import *

from RoadSignsModel import *


############################################################
# Classifier View

class MainView(ZImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                     datasets={"RoadSigns": 0})
    
    self.model_loaded = False
    self.image_size = (RoadSignsModel.IMAGE_WIDTH, RoadSignsModel.IMAGE_HEIGHT)
        
    # Target image to be classified by this classifer.
    self.image       = None
    
    self.classes = self.get_class_names()
    
    self.model = RoadSignsModel(self.dataset_id, mainv=self)
    if self.model.is_trained():
      self.model.create()
      
      # Load trained model provided trained.
      self.model.load()
      self.model.compile()
      #self.model.evaluate()
      self.model_loaded = True
    else:
      print("You have to create a model file and weight file")
      print("Please run: python ImageModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "RoadSignsClassifier", 
           "Model/Weight File Missing.\nPlease run: python RoadSignsModel.py " + str(self.dataset_id))

    self.show()


  def classify(self):
    self.write("------------------------------------------------------------")
    self.write("classify start")
    self.write(self.filename)
    prediction = self.model.predict(self.image)
    
    # Get top five pairs of score and classname 
    result = self.get_top_five(prediction, self.classes)
    self.write("Predictions:")
    for score, name in result:
      self.write("  {:.4f}  {}".format(score, name))

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
    
