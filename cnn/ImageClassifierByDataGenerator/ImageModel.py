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

# 2019/04/30
# 2019/09/13 Updated

# encodig: utf-8

import sys
import os
import cv2
import time
import traceback

from keras.preprocessing.image import ImageDataGenerator

from keras.utils import np_utils
 
sys.path.append('../../')

from SOL4Py.ZMain    import *
from SOL4Py.ZMLModel import *

from SOL4Py.keras.ZSimpleSequentialModel import *
from SOL4Py.keras.ZEpochChangeNotifier import *


############################################################
# Image Model class based on Keras ImageDataGenerator.

class ImageModel(ZMLModel):

  ## Class Variables
  IMAGE_MODEL  = 0

  IMAGE_WIDTH  = 128
  IMAGE_HEIGHT = 128

  TRAIN_DATA_DIR = "./dataset/train"
  VALID_DATA_DIR = "./dataset/valid"

  ##
  # Constructor
  def __init__(self, dataset_id, epochs=10, mainv=None, ipaddress="127.0.0.1", port=7777):
    super(ImageModel, self).__init__(dataset_id, mainv)
    
    self._start(self.__init__.__name__)
    
    self.write("dataset_id:{}, ephochs:{}, mainv:{}".format(dataset_id, epochs, mainv) )
    self.model      = None   # Keras model
    self.dataset_id = dataset_id 
    self.dataset    = None
    self.epochs     = epochs
    self.set_dataset_id(dataset_id)

    self.callbacks = [ZEpochChangeNotifier(ipaddress, port, self.__class__.__name__, self.epochs+10)]
    self.classes   = sorted( os.listdir(self.TRAIN_DATA_DIR) )
    self.n_classes = len(self.classes)

    self.image_width  = self.IMAGE_WIDTH
    self.image_height = self.IMAGE_HEIGHT
    
    self.IMAGE_SIZE = (self.image_width, self.image_height)

    self._end(self.__init__.__name__)



  def set_dataset_id(self, dataset_id):
    self._start(self.set_dataset_id.__name__)
    self.dataset_id   = dataset_id
    
    self.weight_file  = self.__class__.__name__ + "_" + str(self.dataset_id) + ".h5"
    self.n_classes    = 0
    self.write("weight_file  " + self.weight_file)
   
    self._end(self.set_dataset_id.__name__)


  def build(self):
    self.write("====================================")
    self._start(self.build.__name__)
    
    if self.is_trained() != True:
      try:        
        # Create ImageDataGenerator
        self.create_generator()
        self.create_flow()
        
        self.create()
        self.compile()
        
        self.train()
        #self.evaluate()
        self.save()
        self.plot()
         
      except:
        traceback.print_exc()
      
    self._end(self.build.__name__)
     

  def create_generator(self):
    self._start(self.create_generator.__name__)

    self.train_data_generator = ImageDataGenerator(
                                        rescale            = 1.0/255.0,
                                        rotation_range     = 20,    
                                        width_shift_range  = 1.0, 
                                        height_shift_range = 0.3,
                                        shear_range        = 0.4,       
                                        zoom_range         = 0.3,        
                                        brightness_range   = [0.7,1.2],
                                        channel_shift_range= 2.0, 
                                        horizontal_flip    = True,
                                        vertical_flip      = False)

    self.valid_data_generator  = ImageDataGenerator( 
                                        rescale            = 1.0/255.0)

    self._end(self.create_generator.__name__)



  def create_flow(self):
    self._start(self.create_flow.__name__)

    self.BATCH_SIZE = 32
    
    self.CLASS_MODE = "categorical"
     
    self.COLOR_MODE     = "rgb"
    self.classes        = sorted( os.listdir(self.TRAIN_DATA_DIR) )
    self.n_classes = len(self.classes)

    self.train_flow = self.train_data_generator.flow_from_directory(
         self.TRAIN_DATA_DIR,
         target_size = self.IMAGE_SIZE,
         batch_size  = self.BATCH_SIZE,
         class_mode  = self.CLASS_MODE,
         color_mode  = self.COLOR_MODE,
         shuffle     = True)

    self.valid_flow = self.valid_data_generator.flow_from_directory(
         self.VALID_DATA_DIR,
         target_size = self.IMAGE_SIZE,
         batch_size  = self.BATCH_SIZE,
         class_mode  = self.CLASS_MODE,
         color_mode  = self.COLOR_MODE,
         shuffle     = True)

    self._end(self.create_flow.__name__)


  # Create a sequential model
  def create(self):
    self._start(self.create.__name__)
    input_shape = (self.image_width, self.image_height, 3)
    self.model = ZSimpleSequentialModel(input_shape, self.n_classes)
    self._end(self.create.__name__)


  def compile(self):
    self._start(self.compile.__name__)  
    self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    self._end(self.compile.__name__)


  def train(self, train_steps =100, valid_steps = 20):  
    self._start(self.train.__name__)
    start = time.time()

    self.train_steps = train_steps
    self.valid_steps = valid_steps

    self.model.fit_generator(
             self.train_flow,
             steps_per_epoch  = self.train_steps,      
             epochs           = self.epochs,
             callbacks        = self.callbacks,
             validation_data  = self.valid_flow,
             validation_steps = self.valid_steps)
    
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self.model.summary()
    self._end(self.train.__name__)


  def predict(self, image):
    #self._start(self.predict.__name__)
    
    prediction = self.model.predict(image)
    
    #self.write("Prediction: {}".format(prediction))
 
    #self._end(self.predict.__name__)
    return prediction


  def predict_classes(self, image):
    self._start(self.predict_classes.__name__)
    classes = self.model.predict_classes(image)
    self.write("Predicted classes{}".format(classes))
    self._end(self.predict_classes.__name__)
    return classes


  def save(self):
    self._start(self.save.__name__)
        
    self.model.save_weights(self.weight_file)
    self.write("Saved weight file {}".format(self.weight_file))
    self._end(self.save.__name__)



  def load(self):
    self._start(self.load.__name__)

    try:                
      self.model.load_weights(self.weight_file)
      self.write("Loaded a weight file:{}".format(self.weight_file))

    except:
      self.write( formatted_traceback() )

    self._end(self.load.__name__)


  def get_model(self):
    return self.model


  def is_trained(self):
    rc = False
    
    if os.path.isfile(self.weight_file) == True:
      rc = True
    return rc



  def plot(self, filename=None):
    from keras.utils import plot_model
    if filename == None:
       filename = self.__class__.__name__ + "_model.png"
    plot_model(self.model, to_file=filename,show_shapes=True)


############################################################
#    

if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
   
    dataset_id = ImageModel.IMAGE_MODEL
    
    epochs     = 10
    
    if len(sys.argv) >= 2:
      dataset_id = int(sys.argv[1])
      
    if len(sys.argv) >= 3:
      epochs = int(sys.argv[2])

    model = ImageModel(dataset_id, epochs, None)
    model.build()

  except:
    traceback.print_exc()

