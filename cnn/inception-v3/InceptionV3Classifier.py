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

# 2019/03/05
# 2019/09/13 Updated load_file method not to use a temporary image file.

# Inception V3 model for Keras.
# See: https://github.com/keras-team/keras-applications/blob/master/keras_applications/inception_v3.py

#  InceptionV3Classifier.py

# encodig: utf-8

import sys
import os
import time
import traceback
import numpy as np

#from keras.utils import np_utils
from tensorflow.python.keras.utils import np_utils

from tensorflow.python.keras.preprocessing.image import image, load_img, img_to_array
from tensorflow.python.keras.applications.inception_v3 import InceptionV3
from tensorflow.python.keras.applications.inception_v3 import preprocess_input, decode_predictions
 
sys.path.append('../../')

from SOL4Py.ZImageClassifierView import *

DATASET_InceptionV3 = 0

############################################################
# Classifier View

class MainView(ZImageClassifierView):  
  # Class variables
  
  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                    datasets = {"InceptionV3": DATASET_InceptionV3})

    self.model_loaded = False

    # keras.preprocessing.image
    self.image       = None

    self.image_size = (299, 299)   #2019/09/13 Modified
    
    # Load trained model
    self.write("Loading InceptionV3 Model")
    self.model = InceptionV3(weights='imagenet')
    self.write("Loaded InceptionV3")
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
    self.write("-----------------------------------------------------")
    self.write("classify start")
    self.write(self.filename)

    input = np.stack([self.image]);

    predictions = self.model.predict(input)
    # Get top five predictions
    results = decode_predictions(predictions, top=5)[0]
    self.write("Predictions:")
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
    
