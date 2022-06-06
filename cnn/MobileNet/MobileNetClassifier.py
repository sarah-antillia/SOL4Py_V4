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

# 2019/07/01
# 2019/09/13 Updated load_file method not to use a temporary image file.

#  MobileNetClassifier.py

# MobileNet for Keras
# See:https://keras.io/ja/applications/
# keras.applications.mobilenet.MobileNet(input_shape=None, 
#            alpha=1.0, depth_multiplier=1, dropout=1e-3, include_top=True, weights='imagenet', input_tensor=None, pooling=None, classes=1000)
# model = load_model('mobilenet.h5', custom_objects={
#                   'relu6': mobilenet.relu6})
                   

# encodig: utf-8

import sys
import os
import time
import traceback

from keras.utils import np_utils
from keras.preprocessing.image import image, load_img, img_to_array
from keras.applications.mobilenet import MobileNet
from keras.applications.mobilenetv2 import MobileNetV2

from keras.applications.mobilenet import preprocess_input, decode_predictions
 
sys.path.append('../../')

from SOL4Py.ZImageClassifierView import *

DATASET_MobileNet = 0

############################################################
# Classifier View

class MainView(ZImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                 datasets={"MobileNet": DATASET_MobileNet})

    self.model_loaded = False
    self.image_size   = (224, 224)
    # keras.preprocessing.image
    self.image        = None
    
    #  Load trained model
    self.write("Loading MobileNet Model")
    self.model = MobileNet(weights='imagenet')
    self.write("Loaded MobileNet")
    self.model_loaded = True
    self.show()


  def load_file(self, filename):
    try:
      image_cropper = ZPILImageCropper(filename)
     
      # 1 Crop larget_central square region from an image of filename.
      cropped_image = image_cropper.crop_largest_central_square_region()
      
      # 2 Load an image from the cropped_fle.
      self.image_view.set_image(img_to_array(cropped_image)) 
      self.image_view.update_scale()

      self.set_filenamed_title(filename)
      
      # 3 Resize the cropped_image  
      self.image = cropped_image.resize(self.image_size)
      
      # 4 Convert the self.image to numpy ndarray and remove alpha channel.
      self.image = self.remove_alpha_channel(img_to_array(self.image))

      # 5 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.image)

      # 6 Convert self.image(ndarray) to an input data format applicable to the VGG16 model.
      self.image = preprocess_input(self.image);

    except:
      self.write(formatted_traceback())


  def classify(self):
    self.write("------------------------------------------------------------")

    self.write("classify start")
    self.write(self.filename)
 
    input = np.stack([self.image]);
    
    predictions = self.model.predict(input)
    results = decode_predictions(predictions, top=5)[0]
    for result in results:
      self.write(str(result))

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
    
