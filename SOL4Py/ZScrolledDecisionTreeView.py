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

#  ZScrolledDecisionTreeView.py

# encodig: utf-8

import sys
import os
import traceback
import time
from sklearn import tree
import pydotplus as pdp

from SOL4Py.ZMain      import *

from SOL4Py.ZImageView import *
from PyQt5.QtWidgets   import *
from PyQt5.QtGui       import *
from PyQt5.QtCore      import *

from SOL4Py.ZScrolledImageView import *

#---------------------------------------------------------------------

class ZScrolledDecisionTreeView(ZScrolledImageView):

  def __init__(self, parent, x, y, width, height, keepAspectRatio=True):
    super(ZScrolledDecisionTreeView, self).__init__(parent, x, y, width, height, keepAspectRatio)
   
   
  def set_tree(self, decision_tree, feature_names=None, target_names=None):
    ctime = int(time.time() * 1000)
    
    filename = str(ctime) + ".png"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    fullpath = os.path.join(current_dir, filename)
    
    try:
      dot_data = tree.export_graphviz(decision_tree,
                                out_file=None,
                                filled=True, 
                                rounded=True, 
                                feature_names=feature_names, 
                                class_names=target_names, 
                                special_characters=True 
                                )
      self.graph = pdp.graph_from_dot_data(dot_data)

      self.graph.write_png(fullpath)
      self.image_view.load_image(fullpath)
      os.remove(fullpath)

    except:
      print(formatted_traceback())

      
                                
                                