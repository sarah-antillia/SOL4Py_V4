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

# 2019/09/13

#  ZTochImageClassifierView.py

# encodig: utf-8

import sys
import os
import time
import traceback
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
import torchvision
from torchvision import datasets, models, transforms
import json
import numpy as np
from PIL import Image

sys.path.append('../../')

from SOL4Py.ZImageClassifierView import *

############################################################
# Classifier View

class ZTorchImageClassifierView(ZImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height, datasets={"ImageModel": 0}):
    super(ZTorchImageClassifierView, self).__init__(title, x, y, width, height, datasets)
    self.resize = 256
    self.crop   = 224

    pass


  def preprocess(self, image, resize=256, crop=224):
    normalize = transforms.Normalize(
                  mean=[0.485, 0.456, 0.406],
                  std =[0.229, 0.224, 0.225])

    preprocessor = transforms.Compose([
                 transforms.Resize(resize),
                 transforms.CenterCrop(crop),
                 transforms.ToTensor(),
                 normalize
                 ])
    return preprocessor(image)


  def image_crop(self, image, resize=256, crop=224):
    crop_preprocessor = transforms.Compose([
       transforms.Resize(resize),
       transforms.CenterCrop(crop)
    ])
    return crop_preprocessor(image)


  def load_file(self, filename):
    self.ndarray = None

    try:      
      # 1 Open an original image file by PIL Image class.
      self.image = Image.open(filename)
            
      array = np.array(self.image)

      self.image_view.set_image(np.array(self.image)) 
      self.image_view.update_scale()  #2019/09/13

      # <modified date="2019/09/13">
      array = self.remove_alpha_channel(array)
      self.image = Image.fromarray(np.uint8(array))
      #</modified>
      
      self.image_tensor = self.preprocess(self.image, self.resize, self.crop)
      self.image_tensor.unsqueeze_(0)
  
      self.set_filenamed_title(filename)
      
      # 2 Crop the image.  
      self.cropped_image = self.image_crop(self.image, self.resize, self.crop)
      
      # 3 Convert the self.image to numpy ndarray. 
      self.ndarray  = np.array(self.cropped_image)

      # 4 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.ndarray)

    except:
      self.write(formatted_traceback())


  def classify(self):
    self.write("------------------------------------------------------------")
    self.write("classify start.")
    self.write(self.filename)

    predictions = self.model(Variable(self.image_tensor))

    predictions = nn.functional.softmax(predictions, dim=1)
    
    TOP_FIVE = 5
    # Get top 5 predictions
    results = predictions.topk(TOP_FIVE)
    #for result in results:
    #  self.write("result {}".format(result))

    scores   = results[0].data.numpy()
    classids = results[1].data.numpy()
    maxid    = classids[0]

    score    = scores[0]
    for i in range(TOP_FIVE):
      label    = self.classes[maxid[i]]
      prob     = score[i]
      self.write("({},  {})".format(label, prob))

    self.write("Classify end.")


 
############################################################
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = ZImageClassifierView(app_name, 40, 40, 900, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()
    
