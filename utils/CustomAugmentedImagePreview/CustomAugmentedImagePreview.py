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

#  CustomAugmentedImagePreview.py

# 2019/07/16 

# encodig: utf-8

import sys
import os
import traceback
import errno

sys.path.append('../../')

from SOL4Py.ZApplicationView  import *
from SOL4Py.ZImageView        import *
from SOL4Py.ZPushButton       import *
from SOL4Py.ZScaleComboBox    import *
from SOL4Py.ZHorizontalLayouter import *

from SOL4Py.ZVerticalPane    import *
from SOL4Py.ZLabeledCheckBox  import *
from SOL4Py.ZLabeledDoubleSpinBox  import *
from SOL4Py.opencv.ZOpenCVCroppedImageReader import *
from SOL4Py.ZCustomImageDataGenerator  import *


class MainView(ZApplicationView):

  IMAGE_COUNT = 25
  IMAGE_COUNT_PERLINE= 5
  CROP_SIZE   = 224
    
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
    
    self.filename = "./girl.jpg"

    # 1. Create our default ZCutomImageDataGenerator with rotation_range
    self.generator = self.create_generator()


    # 2 Create an inner widget.
    self.inner = QWidget(self.main_layouter)
    
    # 3 Set QSizePolicy.Expanding to the self.inner
    self.inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    # 4 Create a grid layout for the inner widget.
    self.grid  = QGridLayout(self.inner)
    
    # 5 Add an instance of ZImageView to the grid.

    try:
      self.size = (self.CROP_SIZE, self.CROP_SIZE)
      self.image = Image.open(self.filename)
      
      # 6 Get flow from the self.generator
      flow  = self.generator.flow(self.image, n_augmentation=self.IMAGE_COUNT)
    
      # 7 Get generated images from the flow.  
      for i in range(self.IMAGE_COUNT):
        # 8 Create an instance of ZImageView
        self.image_views[i] = ZImageView(self, 0, 0, 300, 300)
        
        # 9 Get a generated image from the flow.
        cropped_image = next(flow)
        
        generated = np.asarray(cropped_image)
        
        self.image_views[i].set_image(generated)
        self.image_views[i].rescale(self.scale)
        x = int(i % self.IMAGE_COUNT_PERLINE)
        y = int(i / self.IMAGE_COUNT_PERLINE)
        self.grid.addWidget(self.image_views[i], y, x)

      self.set_filenamed_title(self.filename)

    except:
      traceback.print_exc()

    # 10 Add the inner to the self.
    self.add(self.inner)

    # 11 Add scale_changed callback to the self.scale_combobox.
    self.scale_combobox.add_activate_callback(self.scale_changed)
    
    self.show()


  def create_generator(self):
    # Create an instance ZImageDataGenerator.
    
    return ZCustomImageDataGenerator(crop_size=self.CROP_SIZE,
                                     rotation_angle    = self.rotation_range.get_value(),
                                     left_top_shift    = (self.left_shift_range.get_value(), self.top_shift_range.get_value()),
                                     shrink_ratio      = (self.width_shrink_range.get_value(), self.height_shrink_range.get_value()),

                                     contrast          = self.contrast.get_value(),
                                     saultpepper_noise = self.saultpepper_noise.get_value(),
                                     horizontal_flip   = self.horizontal_flip.is_checked(),
                                     vertical_flip     = self.vertical_flip.is_checked())


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
                                         0, 20.0,    10.0,  step=1.0)
    self.left_shift_range      = ZLabeledDoubleSpinBox(self.vpane, "left_shift_range", 
                                         0, 20.0,   10.0,   step=1.0)
    self.top_shift_range       = ZLabeledDoubleSpinBox(self.vpane, "top_shift_range", 
                                         0, 20.0,  10.0,    step =1.0)
    self.width_shrink_range    = ZLabeledDoubleSpinBox(self.vpane, "width_shrink_range", 
                                         0.80, 0.99,  0.90, step=0.01)
    self.height_shrink_range   = ZLabeledDoubleSpinBox(self.vpane, "height_shrink_range", 
                                         0.80, 0.99,  0.90, step=0.01)
    #self.channel_shift_range  = ZLabeledDoubleSpinBox(self.vpane, "channel_shift", 
    #                                    0, 3.0,   2.0,     step=0.1)
    self.contrast              = ZLabeledDoubleSpinBox(self.vpane, "contrast", 
                                         0.01, 0.06, 0.02,  step=0.01)
    self.saultpepper_noise     = ZLabeledDoubleSpinBox(self.vpane, "saultpepper_noise", 
                                         0.01, 0.05, 0.02,  step=0.01)
    self.horizontal_flip       = ZLabeledCheckBox(self.vpane,  "horizontal_flip") 
    #self.horizontal_flip.set_check()
    
    self.vertical_flip         = ZLabeledCheckBox(self.vpane,  "vertical_flip") 

    self.vpane.add(self.rotation_range)
    self.vpane.add(self.left_shift_range)
    self.vpane.add(self.top_shift_range)
    self.vpane.add(self.width_shrink_range)
    self.vpane.add(self.height_shrink_range)

    self.vpane.add(self.contrast)
    self.vpane.add(self.saultpepper_noise)
    self.vpane.add(self.horizontal_flip)
    self.vpane.add(self.vertical_flip)
    self.set_right_dock(self.vpane)


  # Callback to the preview PushButton
  def do_preview(self):
    self.inner.hide()

    try:
      self.size = (self.CROP_SIZE, self.CROP_SIZE)
      self.image = Image.open(self.filename)
      
      self.generator = self.create_generator()
     
      # 1 Get flow from the self.generator
      flow  = self.generator.flow(self.image, n_augmentation=self.IMAGE_COUNT)
    
      # 2 Get generated images from the flow.  
      for i in range(self.IMAGE_COUNT):
        
        # 3 Get a generated image from the flow.
        cropped_image = next(flow)
        
        generated = np.asarray(cropped_image)
        
        self.image_views[i].set_image(generated)
        self.image_views[i].rescale(self.scale)
        x = int(i % self.IMAGE_COUNT_PERLINE)
        y = int(i / self.IMAGE_COUNT_PERLINE)
        self.grid.addWidget(self.image_views[i], y, x)

      self.set_filenamed_title(self.filename)

    except:
      traceback.print_exc()
  
    self.grid.update()
    self.inner.show()



  def load_file(self, filename):    
    self.do_preview()


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
    self.filename, _ = QFileDialog.getOpenFileName(self,"FileOpenDialog", "",
                     "All Files (*);;Image Files (*.png;*jpg;*.jpeg)", options=options)
    if self.filename:
      self.load_file(self.filename)
      self.set_filenamed_title(self.filename)


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
        self.generator = self.create_generator()

        # Get a flow from the self.generator
        flow  = self.generator.flow_from_directory(self.filename, 
                      save_folder = folder,
                      save_format=  "jpg",
                      n_augmentation=self.IMAGE_COUNT)

        # Get generated images from the flow.  
        for i in flow:  
          image = next(flow)
          print("generated {} image size: {}".format(i, image.size))
          
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

