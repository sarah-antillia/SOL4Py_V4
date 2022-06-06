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

# 2019/05/10

# ZSimpleAutoEncoderModel.py

# encodig: utf-8

# This class is based on https://blog.keras.io/building-autoencoders-in-keras.html


from tensorflow.python.keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from tensorflow.python.keras.models import Model
#from keras import backend as K

class ZSimpleAutoEncoderModel(Model):

  def __init__(self, input_shape):
    self.input_image  = Input(shape=input_shape)
    self.decoded = self.build(self.input_image)
    Model.__init__(self, self.input_image, self.decoded)


  def build(self, input_image):
    encoded = self.encode(input_image)
    decoded = self.decode(encoded)
    return decoded 
 
  # This is an encode method for MNIST
  # If required, please redefine your own encode method in a subclass derived from this class.
  def encode(self, input_image):
    x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_image)
    x = MaxPooling2D((2, 2),                  padding='same')(x)
    x = Conv2D( 8, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2),                  padding='same')(x)
    x = Conv2D( 8, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2),            padding='same')(x)
    return encoded

  # This is a deocoder or MNIST
  # If required, please redefine your own decode method in a subclass derived from this class.
  def decode(self, encoded):
    x = Conv2D( 8, (3, 3), activation='relu',         padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D( 8, (3, 3), activation='relu',         padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(16, (3, 3), activation='relu'                        )(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
    
    return decoded

 

