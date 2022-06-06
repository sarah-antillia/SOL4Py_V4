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

#  ZMLModel.py
 
# Machine Learning Model class.
#
# This may be used a base class to derive a class of classification and regression model.


# encodig: utf-8

import sys
import os
import traceback
import pickle


#---------------------------------------------------------------------
class ZMLModel:

  ##
  # Constructor
  def __init__(self, dataset_id, mainv, stdout=True):
    self.view = mainv
    self.dataset_id = dataset_id
    self.dataset = None
    self.model   = None
    self.model_filename = None
    self.stdout  = stdout
    
  # Define your own run method in a subclass derived from this class.
  def run(self):
    pass


  # Define your own load_dataset method in a subclass derived from this class.
  def load_dataset(self):
    self.dataset = None
    pass


  # Define your own create method in a subclass derived from this class.
  def create(self):
    pass
   
  def set_dataset_id(self, dataset_id):
    self.dataset_id = dataset_id


  # Set a pkl filename to save a trained result.
  def set_model_filename(self):
    filename = self.__class__.__name__ + "_" + str(self.dataset_id) + ".pkl"
    
    # __file__ will be */SOL4Py directory, becaus this file is in that directory 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(current_dir, "pkl")
    
    try:
      if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
      fullpath = os.path.join(dest_dir, filename)
      self.model_filename = fullpath

    except:
      self.write(formatted_traceback())


  def get_model_filename(self):
    return self.model_filename


  # Define your own build method in a subclass derived from this class.
  def build(self):
    self.model = None
    pass
    
  # Define your own train method in a subclass derived from this class.
  def train(self):
    pass


  # Check the self.model_filename pkl file exits
  def trained(self):
    return os.path.isfile(self.model_filename)


  def save(self):
    with open(self.model_filename, "wb") as pkl:
      pickle.dump(self.model, pkl)


  def load(self):
    with open(self.model_filename, "rb") as pkl:
      self.model = pickle.load(pkl)

  
  # Define your own predic method in a subclass derived from this class.
  def predict(self):
    pass

  # Define your own visualize method in a subclass derived from this class, if needed.
  def visualize(self):
    pass


  # Write a string of the form "ClassName::method start" to the self.view.
  def _start(self, string):
    message = self.__class__.__name__ + "::" + string + " start"
    if self.view != None:
      self.view.write(message)
      if self.stdout:
        print(message)
    else:
      print(message)
      
      
  # Write a string of the form "ClassName::method end" to the self.view.
  def _end(self, string):
    message = self.__class__.__name__ + "::" + string + " end\n"
    if self.view != None:
      self.view.write(message)
      if self.stdout:
        print(message)
    else:
      print(message)
 
  def write(self, string):
    if self.view != None:
      self.view.write(string)
      if self.stdout:
        print(string)
    else:
      print(string)


  def save_class_names(self, classes, path = "./class_names.txt"):
    try:
      with open(path, "w") as file:
        for name in classes:
          #print(name)
          file.write("{}\n".format(name))    
      print("Saved classes to {}".format(path))
    except:
      traceback.print_exc()
  

