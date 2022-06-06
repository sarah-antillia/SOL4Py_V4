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

# 2018/09/20
# 2019/09/13

#  MNISTClassifier.py

# encodig: utf-8

import sys
import os
import time
import traceback

sys.path.append('../../')

from SOL4Py.ZImageClassifierView import *

from MNISTModel import *

MNIST         = 0
FASHION_MNIST = 1


############################################################
# Classifier View

class MainView(ZImageClassifierView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height,
                 datasets = {"MNIST": MNIST, "FashionMNIST": FASHION_MNIST})
 
    self.class_names_set = [None, None]
    
    # ndarry image datat created from keras.preprocessing.image
    self.image       = None
                            
    self.class_names_set[MNIST] = ["0", "1", "2", "3", "4",
                                   "5", "6", "7", "8", "9"]
    self.class_names_set[FASHION_MNIST]  =['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    self.image        = None
    self.model_loaded = False
    self.image_size   = (28, 28)
       
    # Load the trained model    
    self.model = MNISTModel(self.dataset_id, epochs = 10, mainv=self)
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create() 

      self.model.load()
      self.model.compile()
      self.model.evaluate()
      self.model_loaded = True
    else:
      print("You have to create a model file and weight file")
      print("Run: python MNISTModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "MNIST", 
           "Model/Weight File Missing.\nPlease run: python MNISTModel.py " + str(self.dataset_id))
  
    self.show()


  def datasets_activated(self, text):
    self.dataset_id = self.datasets[text]
    title = self.get_title()
    self.setWindowTitle(text + " - " + title)
    self.model.set_dataset_id(self.dataset_id)
      
    self.classifier_button.setEnabled(False)
    
    if self.model.is_trained():
      self.model.load_dataset()
      self.model.create()    # 2019/09/13
      self.model.load()
      self.model.compile()
      self.model.evaluate()
      self.model_loaded =True        
      QMessageBox.information(self, "MNIST", 
           "OK: MNIST Model/Weight files loaded")

    else:
      print("You have to create a model file and a weight file.")
      print("Please run: python MNISTModel.py " + str(self.dataset_id))
      QMessageBox.warning(self, "MNIST", 
           "Model/Weight files missing.\nPlease run: python MNISTModel.py " + str(self.dataset_id))


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
      
      # 4 Conver the self.image to a gray-scale image
      self.image = self.image.convert('L')

      self.image =  img_to_array(self.image)
 
      # 5 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.image)

      # 6 Convert self.image in range[0-1.0]
      self.image = self.image.astype('float32')/255.0
      
      # 7 Expand the dimension of the self.image 
      self.image = np.expand_dims(self.image, axis=0) 

    except:
      self.write(formatted_traceback())


  def classify(self):
    self.write("------------------------------------------------------------")
    self.write("classify start")
    self.write(self.filename)

    try:
      prediction = self.model.predict(self.image)            
      pred = np.argmax(prediction, axis=1)
      class_names = self.class_names_set[self.dataset_id]
        
      if pred >0 or pred <len(class_names):
        self.write("Prediction:" + class_names[int(pred)])

    except:
      self.write(formatted_traceback())
      
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
    
