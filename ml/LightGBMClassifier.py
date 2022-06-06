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

# 2018/09/01

#  LightGBMClassifier.py

# encodig: utf-8

import sys
import os
import time
import traceback
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import numpy as np

import pickle
import lightgbm as lgb

from sklearn.model_selection import train_test_split
#from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix, classification_report
 
sys.path.append('../')

from SOL4Py.ZMLModel import *
from SOL4Py.ZApplicationView import *
from SOL4Py.ZLabeledComboBox import *
from SOL4Py.ZPushButton      import *
from SOL4Py.ZVerticalPane    import * 

from SOL4Py.ZTabbedWindow import *
from SOL4Py.ZScalableScrolledFigureView import *
from SOL4Py.ZScalableScrolledFigureView import *

# sklearn datasets

Iris        = 0
Digits      = 1
Wine        = 2
BreastCancer = 3

############################################################
# Classifier Model class

class LightGBMClassifierModel(ZMLModel):

  ##
  # Constructor
  def __init__(self, dataset_id, mainv):
    super(LightGBMClassifierModel, self).__init__(dataset_id, mainv)

  def run(self):
    self.write("====================================")
    self._start(self.run.__name__)    
    try: 
      self.load_dataset()

      self.build()
      self.train()
      self.save()
        
      self.predict()
      self.visualize() 
      
    except:
      traceback.print_exc()
    self._end(self.run.__name__)


  def load_dataset(self):
    self._start(self.load_dataset.__name__)
    
    if self.dataset_id == Iris:
       self.dataset= datasets.load_iris()
       self.write("loaded iris dataset")

    if self.dataset_id == Digits:
       self.dataset= datasets.load_digits()
       self.write("loaded Digits dataset")
  
    if self.dataset_id == Wine:
       self.dataset= datasets.load_wine()
       self.write("loaded Wine dataset")

    if self.dataset_id == BreastCancer:
       self.dataset= datasets.load_breast_cancer()
       self.write("loaded BreastCancer dataset")
       
    attr = dir(self.dataset)
    self.write("dir:" + str(attr))
    if "feature_names" in attr:
      self.write("feature_names:" + str(self.dataset.feature_names))
    if "target_names" in attr:
      self.write("target_names:" + str(self.dataset.target_names))
      
    self.set_model_filename()
    self.view.description.setText(self.dataset.DESCR)
   
    X, y = self.dataset.data, self.dataset.target
    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    self._end(self.load_dataset.__name__)
 
 
  def build(self):
    self._start(self.build.__name__)
   
    self.model = lgb.LGBMClassifier(
                        objective='multiclass',
                        num_class = 2,
                        num_leaves = 31,
                        learning_rate=0.1,
                        min_child_samples=10,
                        n_estimators=100)

    self._end(self.build.__name__)


  def train(self):
    print("---------------train ")
    self._start(self.train.__name__)
    start = time.time()

    # Class fit method of the classifier
    self.model.fit(self.X_train, self.y_train,
                eval_set=[(self.X_test, self.y_test)],
                eval_metric='multi_logloss',
                early_stopping_rounds=10)
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    
    self._end(self.train.__name__)


  def predict(self):
    self._start(self.predict.__name__)
    self.pred_test  = self.model.predict(self.X_test, num_iteration=self.model.best_iteration_)
    report = str (classification_report(self.y_test, self.pred_test) )
    self.write(report)
    self._end(self.predict.__name__)


  def visualize(self):
    cmatrix = confusion_matrix(self.y_test, self.pred_test)
    self.view.visualize(cmatrix)
    

############################################################
# Classifier View

class MainView(ZApplicationView):  
  # Class variables

  # ClassifierView Constructor
  def __init__(self, title, x, y, width, height):
    super(MainView, self).__init__(title, x, y, width, height)
    self.font        = QFont("Arial", 10)
    self.setFont(self.font)
    
    # 1 Add a labeled combobox to top dock area
    self.add_datasets_combobox()
    
    # 2 Add a textedit to the left pane of the center area.
    self.text_editor = QTextEdit()
    self.text_editor.setLineWrapColumnOrWidth(600)
    self.text_editor.setLineWrapMode(QTextEdit.FixedPixelWidth)

    # 3 Add a description to display dataset.DESCR.
    self.description = QTextEdit()
    self.description.setLineWrapColumnOrWidth(600)
    self.description.setLineWrapMode(QTextEdit.FixedPixelWidth)
    
    # 4 Add a tabbed_window to the tabbed_window.
    self.tabbed_window = ZTabbedWindow(self, 0, 0, width/2, height)

    # 5 Add a figure_view to the tabbed_window.
    self.figure_view = ZScalableScrolledFigureView(self, 0, 0, width/2, height)
       
    self.add(self.text_editor)
    self.add(self.tabbed_window)
    
    self.tabbed_window.add("Description",     self.description)
    self.tabbed_window.add("ConfusionMatrix", self.figure_view)
    self.figure_view.hide()
 
    self.show()
    
    
  def add_datasets_combobox(self):
    self.dataset_id = Iris
    self.datasets_combobox = ZLabeledComboBox(self, "Datasets", Qt.Horizontal)
    
    # We use the following datasets of sklearn to test XGBClassifier.
    self.datasets = {"Iris": Iris, "Digits": Digits, "Wine": Wine, "BreastCancer": BreastCancer}
    title = self.get_title()
    self.setWindowTitle( "Iris" + " - " + title)
    
    self.datasets_combobox.add_items(self.datasets.keys())
    self.datasets_combobox.add_activated_callback(self.datasets_activated)
    self.datasets_combobox.set_current_text(self.dataset_id)

    self.start_button = ZPushButton("Start", self)
    self.clear_button = ZPushButton("Clear", self)

    self.start_button.add_activated_callback(self.start_button_activated)
    self.clear_button.add_activated_callback(self.clear_button_activated)

    self.datasets_combobox.add(self.start_button)
    self.datasets_combobox.add(self.clear_button)
    
    self.set_top_dock(self.datasets_combobox)
  
          
  def write(self, text):
    self.text_editor.append(text)
    self.text_editor.repaint()
    
  def datasets_activated(self, text):
    self.dataset_id = self.datasets[text]
    title = self.get_title()
    self.setWindowTitle(text + " - " + title)

  def start_button_activated(self, text):
    self.model = LightGBMClassifierModel(self.dataset_id, self)
    self.start_button.setEnabled(False)    
    self.clear_button.setEnabled(False)
    try:
      self.model.run()
    except:
      pass
    self.start_button.setEnabled(True)
    self.clear_button.setEnabled(True)
    
    
  def clear_button_activated(self, text):
    self.text_editor.setText("")
    self.description.setText("")
    self.figure_view.hide()
    plt.close()


  def visualize(self, cmatrix):
    self.figure_view.show()

    plt.close()

    sns.set()
    df = pd.DataFrame(cmatrix)
    sns.heatmap(df, annot=True, fmt="d")
    # Set a new figure to the figure_view.
    self.figure_view.set_figure(plt)

############################################################
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 800, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()
    
