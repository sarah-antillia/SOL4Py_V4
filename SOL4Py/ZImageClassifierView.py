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


#  ZImageClassifierView.py

# encodig: utf-8

import sys
import os
import time
import traceback
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf

sys.path.append('../../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZLabeledComboBox import *
from SOL4Py.ZPushButton      import *
from SOL4Py.ZVerticalPane    import *
from SOL4Py.ZPILImageCropper import *
 
from SOL4Py.ZScrolledPlottingArea import *
from SOL4Py.ZScalableScrolledImageView import *
from SOL4Py.ZTabbedWindow import *



############################################################
# Classifier View

class ZImageClassifierView(ZApplicationView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height, datasets={"ImageModel": 0}):
    super(ZImageClassifierView, self).__init__(title, x, y, width, height)
    self.font        = QFont("Arial", 10)
    self.setFont(self.font)
    
    self.datasets = datasets
    
    self.model_loaded = False
    
    self.class_names_set = [None, None]

    # Image filename to be classified
    self.filename     = None
    
    # Target image to be classified
    self.image       = None

    # 1 Add a labeled combobox to top dock area
    self.add_datasets_combobox()
    
    # 2 Add a textedit to the left pane of the center area.
    self.text_editor = QTextEdit()
    self.text_editor.setLineWrapColumnOrWidth(600)
    self.text_editor.setLineWrapMode(QTextEdit.FixedPixelWidth)
    self.text_editor.setGeometry(0, 0, width/2, height)
    
    # 3 Add a tabbed_window the rigth pane of the center area.
    self.tabbed_window = ZTabbedWindow(self, 0, 0, width/2, height)
    
    # 4 Add a imageview to the tabbed_window.
    self.image_view = ZScalableScrolledImageView(self, 0, 0, width/3, height/3)   
    self.tabbed_window.add("SourceImage", self.image_view)
    
    # 5 Add a test_imageview to the right pane of the center area.
    self.test_image_view = ZScalableScrolledImageView(self, 0, 0, width/3, height/3)   
    self.tabbed_window.add("TestImage", self.test_image_view)

    self.add(self.text_editor)
    self.add(self.tabbed_window)
    

  def add_datasets_combobox(self):
    datasetkey = list(self.datasets.keys())[0]
    self.dataset_id = self.datasets[datasetkey]
    print("Current combobox item {} {}".format(datasetkey, self.dataset_id))
    
    self.datasets_combobox = ZLabeledComboBox(self, "Datasets", Qt.Horizontal)
    self.datasets_combobox.setFont(self.font)
    
    title = self.get_title()
    
    self.setWindowTitle(self.__class__.__name__ + " - " + title)
    
    self.datasets_combobox.add_items(self.datasets.keys())
    self.datasets_combobox.add_activated_callback(self.datasets_activated)
    self.datasets_combobox.set_current_text(self.dataset_id)

    self.classifier_button = ZPushButton("Classify", self)
    self.classifier_button.setEnabled(False)

    self.clear_button = ZPushButton("Clear", self)
    
    self.classifier_button.add_activated_callback(self.classifier_button_activated)
    self.clear_button.add_activated_callback(self.clear_button_activated)

    self.datasets_combobox.add(self.classifier_button)
    self.datasets_combobox.add(self.clear_button)
    
    self.set_top_dock(self.datasets_combobox)


  def write(self, text):
    self.text_editor.append(text)
    self.text_editor.repaint()


  def datasets_activated(self, text):
    pass


  # Show FileOpenDialog and select an image file.
  def file_open(self):
    if self.model_loaded:
      options = QFileDialog.Options()
      filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
      if filename:
        self.filename = filename
        self.load_file(filename)
        self.classifier_button.setEnabled(True)
    else:
      QMessageBox.warning(self, "ImageClassifier: Weight File Missing", 
           "Please run: python RoadSignsModel.py " + str(self.dataset_id))


  def remove_alpha_channel(self, array):
    shape = array.shape
    if len(shape) ==3:
      w, h, c = shape
      if c == 4:
        #(w, h, 4) -> (w, h, 3)  
        #print("Remove the alpha channel of array")
        array = array[:,:,:3]
    return array
    

  def load_file(self, filename):
    #from keras.preprocessing.image import load_img, img_to_array

    try:
      image_cropper = ZPILImageCropper(filename)
     
      # 1 Crop larget_central square region from an image of filename.
      cropped_image = image_cropper.crop_largest_central_square_region()
      
      # 2 Load an image from the cropped_fle.
      self.image_view.set_image( tf.keras.preprocessing.image.img_to_array(cropped_image)) 
      self.image_view.update_scale()
      self.set_filenamed_title(filename)
      
      # 3 Resize the cropped_image  
      self.image = cropped_image.resize(self.image_size)
      
      # 4 Convert the self.image to numpy ndarray and remove alpha channel.
      self.image = self.remove_alpha_channel(tf.keras.preprocessing.image.img_to_array(self.image))

      # 5 Set self.nadarryy to the test_image_view.
      self.test_image_view.set_image(self.image)

      # 6 Convert self.image in range[0-1.0]
      self.image = self.image.astype('float32')/255.0
      
      # 7 Expand the dimension of the self.image 
      self.image = np.expand_dims(self.image, axis=0) 
      
      #print(self.image.shape)
      
    except:
      self.write(formatted_traceback())


  def classifier_button_activated(self, text):
    self.classifier_button.setEnabled(False)    
    self.clear_button.setEnabled(False)
    try:
      self.classify()
    except:
      self.write(formatted_traceback())
      
    self.classifier_button.setEnabled(True)
    self.clear_button.setEnabled(True)


  def get_top_five(self, predictions, classes, K=5):
    pred = predictions[0]
    indices = np.argpartition(pred, -K)[-K:]
    results = []
    for i in indices:    
      results.append([pred[i], classes[i]])
    results = sorted(results, reverse=True)
    return results


  def get_class_names(self, path="./class_names.txt"):
    classes = []
    with open(path, "r") as file:
      classes = [s.strip() for s in file.readlines()]
    return classes
 

  def classify(self):
    self.write("------------------------------------------------------------")
    self.write("classify start")
    self.write(self.filename)
    prediction = self.model.predict(self.image)
    
    pred = np.argmax(prediction, axis=1)
    #self.write("Prediction: index " + str(pred))
    class_names = self.model.classes

    if pred >0 or pred <len(class_names):
      self.write("Prediction:" + class_names[int(pred)])

    self.write("classify end")


  def clear_button_activated(self, text):
    self.text_editor.setText("")
    pass
  
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
    
