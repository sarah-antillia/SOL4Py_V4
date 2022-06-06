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

#  AugmentedImagePreview.py

# 2019/04/16 
# 2019/05/20 Updated load_file to be able to show expected augmented images when the preview button is pressed.

# encodig: utf-8

import sys
import os
import traceback
import errno

sys.path.append('../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZImageView        import *
from SOL4Py.ZPushButton       import *
from SOL4Py.ZScaleComboBox    import *
from SOL4Py.ZHorizontalLayouter import *

from SOL4Py.ZVerticalPane    import *
from SOL4Py.ZLabeledCheckBox  import *
from SOL4Py.ZLabeledDoubleSpinBox  import *
from SOL4Py.opencv.ZOpenCVCroppedImageReader import *
#from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

class MainView(ZApplicationView):

  IMAGE_COUNT = 25
  IMAGE_COUNT_PERLINE= 5
  
  # MainView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height, Z.Vertical)

    self.get_layout().setSpacing(0)
    self.scale = 50
    
    self.get_layout().setContentsMargins(0,0,0,0);

    self.scale_combobox = ZScaleComboBox(None, "Scale")
    self.scale_combobox.current_scale(self.scale)
    
    self.add(self.scale_combobox)
    
    self.image_views = [None] * self.IMAGE_COUNT #
    
    filename = "../images/Car_101.png"

    # 1. Create our default ImageDataGenerator with rotation_range
    self.generator = self.create_generator()


    # 2 Create an inner widget.
    self.inner = QWidget(self.main_layouter)
    
    # 3 Set QSizePolicy.Expanding to the self.inner
    self.inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    # 4 Create a grid layout for the inner widget.
    self.grid  = QGridLayout(self.inner)
    
    # 5 Add an instance of ZImageView to the grid.

    try:
      self.size = (224, 224)
      # Get an image cropped with max square region and scaled with self.size
      image = self.load_cropped_scaled_image(filename, self.size)
      
      # (height, width, channles) to (1, height, width, channels)
      self.data = image.reshape((1,) + image.shape)

      # 6 Get flow from the self.generator
      flow  = self.generator.flow(self.data, batch_size=1)
    
      # 7 Get generated images from the flow.  
      for i in range(self.IMAGE_COUNT):
        # 8 Create an instance of ZImageView
        self.image_views[i] = ZImageView(self, 0, 0, 300, 300)
        
        # 9 Get a generated image from the flow.
        batches = next(flow)
        
        generated = batches[0].astype(np.uint8)
        self.image_views[i].set_image(generated)
        self.image_views[i].rescale(self.scale)
        x = int(i % self.IMAGE_COUNT_PERLINE)
        y = int(i / self.IMAGE_COUNT_PERLINE)
        self.grid.addWidget(self.image_views[i], y, x)

      self.set_filenamed_title(filename)

    except:
      traceback.print_exc()

    # 10 Add the inner to the self.
    self.add(self.inner)

    # 11 Add scale_changed callback to the self.scale_combobox.
    self.scale_combobox.add_activate_callback(self.scale_changed)
    
    self.show()


  def create_generator(self):
    # Create an instance ImageDataGenerator from self.*_range's
    
    return tf.keras.preprocessing.image.ImageDataGenerator( 
                                        rotation_range     = self.rotation_range.get_value(),    
                                        width_shift_range  = self.width_shift_range.get_value(), 
                                        height_shift_range = self.height_shift_range.get_value(),
                                        shear_range        = self.shear_range.get_value(),       
                                        zoom_range         = self.zoom_range.get_value(),        
                                        brightness_range   = [self.brightness_low_range.get_value(),
                                                              self.brightness_high_range.get_value()],
                                        channel_shift_range= self.channel_shift_range.get_value(), 
                                        horizontal_flip    = self.horizontal_flip.is_checked(),
                                        vertical_flip      = self.vertical_flip.is_checked())


  def add_control_pane(self, fixed_width=200):
    self.vpane   = ZVerticalPane(self, fixed_width)
    # Create preview PushButton
    self.preview = ZPushButton("Preview", self.vpane)
    self.preview.add_activated_callback(self.do_preview)
 
    self.vpane.add(self.preview)
    self.spacing = QLabel("  ")
    self.vpane.add(self.spacing)
    
    self.label = QLabel("ImageDataGenerator Parameters:")
    self.vpane.add(self.label)
    #self.groupBox.setLayout(self.vpane.get_layout())
    
    self.rotation_range        = ZLabeledDoubleSpinBox(self.vpane, "rotation_range",      
                                         0, 30,    20,   step=1.0)
    self.width_shift_range     = ZLabeledDoubleSpinBox(self.vpane, "width_shift_range", 
                                         0, 2.0,   1.0,  step=0.1)
    self.height_shift_range    = ZLabeledDoubleSpinBox(self.vpane, "height_shift_range", 
                                         0, 2.0,   0.3,  step=0.1)
    self.shear_range           = ZLabeledDoubleSpinBox(self.vpane, "shear_range", 
                                         0, 2.0,   0.4,  step=0.1)
    self.zoom_range            = ZLabeledDoubleSpinBox(self.vpane, "zoom_range", 
                                         0, 2.0,   0.3,  step=0.1)
    self.channel_shift_range   = ZLabeledDoubleSpinBox(self.vpane, "channel_shift", 
                                         0, 3.0,   2.0,  step=0.1)
    self.brightness_low_range  = ZLabeledDoubleSpinBox(self.vpane, "brightness_low_range", 
                                         0.5, 1.0, 0.7,  step=0.1)
    self.brightness_high_range = ZLabeledDoubleSpinBox(self.vpane, "brightness_high_range", 
                                         1.0, 1.5, 1.2,  step=0.1)
    self.horizontal_flip       = ZLabeledCheckBox(self.vpane,  "horizontal_flip") 

    self.vertical_flip         = ZLabeledCheckBox(self.vpane,  "vertical_flip") 

    self.vpane.add(self.rotation_range)
    self.vpane.add(self.width_shift_range)
    self.vpane.add(self.height_shift_range)
    self.vpane.add(self.shear_range)
    self.vpane.add(self.zoom_range)
    self.vpane.add(self.channel_shift_range)
    self.vpane.add(self.brightness_low_range)
    self.vpane.add(self.brightness_high_range)
    self.vpane.add(self.horizontal_flip)
    self.vpane.add(self.vertical_flip)
    
    
    self.set_right_dock(self.vpane)

  # Callback to the preview PushButton
  def do_preview(self):
    self.inner.hide()

    try:
      # 1. Create a new instance of ImageDataGenerator.
      self.generator = self.create_generator()

      # 2 Get a flow from the self.generator
      flow  = self.generator.flow(self.data, batch_size=1)
    
      # 3 Get generated images from the flow.  
      for i in range(self.IMAGE_COUNT):  
        batches = next(flow)
        generated = batches[0].astype(np.uint8)
        self.image_views[i].set_image(generated)
        self.image_views[i].rescale(self.scale)
    except:
      traceback.print_exc()
 
    self.grid.update()
    self.inner.show()

  #2019/05/20 Updated
  def load_file(self, filename):
    self.inner.hide()

    # Get an image cropped with max square region and scaled with scale
    image = self.load_cropped_scaled_image(filename, self.size)
    
    # (height, width, channles) to (1, height, width, channels)
    self.data = image.reshape((1,) + image.shape)

    flow  = self.generator.flow(self.data, batch_size=1)
    for i in range(self.IMAGE_COUNT):  
      batches = next(flow)
      generated = batches[0].astype(np.uint8)
      self.image_views[i].set_image(generated)
      self.image_views[i].rescale(self.scale)
    
    self.grid.update()
    self.inner.show()


  def load_cropped_scaled_image(self, filename, size):
    reader  = ZOpenCVCroppedImageReader()
    image   = reader.read(filename)
    return  reader.crop_max_square_region(image, size)


  # Scale changed callback
  def scale_changed(self, text):
    text = text.replace("%", "")
    scale = int(text)	# percentage
    
    # Hide self.inner to avoid the flickering of image_views 
    self.inner.hide()
    for i in range(self.IMAGE_COUNT):
      self.image_views[i].rescale(scale)
    
    # You should call update method of self.grid layout
    self.grid.update()
    
    self.inner.show()
 

  def file_open(self):
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if filename:
      self.load_file(filename)
      self.set_filenamed_title(filename)
      
      
  def file_save(self):
    # 1 Show a folderDialog to select a folder to save generated images
    folder = QFileDialog.getExistingDirectory(self,
                                               "OpenFolder",
                                               os.path.expanduser('.'),
                                               QFileDialog.ShowDirsOnly)
    if folder:
      #dir = dir.replace('/', os.sep)
      print("Folder button clicked {}".format(folder))
          
      self.inner.hide()

      try:
        # 1. Create a new instance of ImageDataGenerator.
        self.generator = self.create_generator()

        # 2 Get a flow from the self.generator
        flow  = self.generator.flow(self.data, batch_size=1, 
                      save_to_dir = folder,
                      save_prefix = "gen", 
                      save_format=  "png")
    
        # 3 Get generated images from the flow.  
        for i in range(self.IMAGE_COUNT):  
          batches = next(flow)
          generated = batches[0].astype(np.uint8)
          self.image_views[i].set_image(generated)
          self.image_views[i].rescale(self.scale)
      except:
        traceback.print_exc()
 
      self.grid.update()
      self.inner.show()


#*************************************************
#    
if main(__name__):
  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 800, 640)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()

