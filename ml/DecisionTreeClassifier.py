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

#  DecisionTreeClassifier.py
# http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
# See also:
# https://github.com/scikit-learn/scikit-learn/blob/f0ab589f/sklearn/tree/tree.py#L515

# encodig: utf-8

import sys
import os
import time
import traceback
import pandas as pd
import seaborn as sns
import pydotplus
import matplotlib.pyplot as plt
import numpy as np
from sklearn.tree import export_graphviz

from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix, classification_report
 
sys.path.append('../')

from SOL4Py.ZApplicationView import *
from SOL4Py.ZLabeledComboBox import *
from SOL4Py.ZPushButton      import *
from SOL4Py.ZVerticalPane    import * 
from SOL4Py.ZTabbedWindow    import *
from SOL4Py.ZMLModel import *
from SOL4Py.ZScalableScrolledFigureView import *
from SOL4Py.ZScalableScrolledDecisionTreeView import*

Iris         = 0
Digits       = 1
Wine         = 2
BreastCancer = 3


############################################################
# Classifier Model class

class DecisionTreeClassifierModel(ZMLModel):

  ##
  # Constructor
  def __init__(self, dataset_id, mainv):
    super(DecisionTreeClassifierModel, self).__init__(dataset_id, mainv)
        
  def run(self):
    self.write("====================================")
    self._start(self.run.__name__)
    try:
      # 1 Load dataset
      self.load_dataset()
      
      # 2 Load or create model
      if self.trained():
        # 2.1 if trained, load a trained model pkl file
        self.load()
      else:
        # 2.2 else create a model, and train and save it
        self.build()
        self.train()
        self.save()
        
      # 3 Predict for test_data
      self.predict()
      
      # 4 Visualize the prediction
      self.visualize() 
 
    except:
      traceback.print_exc()
    self._end(self.run.__name__ )
     
     
  def load_dataset(self):
    self._start(self.load_dataset.__name__ )
    
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
    self.model = tree.DecisionTreeClassifier(random_state=0)
    self._end(self.build.__name__)


  def train(self):  
    self._start(self.train.__name__)
    start = time.time()

    params = {'max_depth':range(3,20)}

    grid_search = GridSearchCV(self.model, param_grid=params, n_jobs=4)
    grid_search.fit(self.X_train, self.y_train)
 
    self.write("GridSearch BestParams " + str(grid_search.best_params_) )
    self.write("GridSearch BestScore "  + str(grid_search.best_score_))
 
    self.model = tree.DecisionTreeClassifier(**grid_search.best_params_)

    # Class fit method of the classifier
    self.model.fit(self.X_train, self.y_train)
 
    elapsed_time = time.time() - start
    elapsed = str("Train elapsed_time:{0}".format(elapsed_time) + "[sec]")
    self.write(elapsed)
    self._end(self.train.__name__)
    

  def predict(self):
    self._start(self.predict.__name__)
    self.pred_test  = self.model.predict(self.X_test)
    report = str (classification_report(self.y_test, self.pred_test) )
    self.write(report)

    self._end(self.predict.__name__)

  def visualize(self):
    cmatrix = confusion_matrix(self.y_test, self.pred_test)
    self.view.visualize(cmatrix, self.model)
 
 
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

    # 3 Add a tabbed_window to the right pane of the center area.
    self.tabbed_window = ZTabbedWindow(self, 0, 0, width/2, height)

    # 4 Add a description text edit.
    self.description = QTextEdit()
    self.description.setLineWrapColumnOrWidth(600)
    self.description.setLineWrapMode(QTextEdit.FixedPixelWidth)
         
    # 5 Add a figure_view to the right pane of the center area.
    self.figure_view = ZScalableScrolledFigureView(self, 0, 0, width/2, height)   
    
    # 6 Add a figure_view to the right pane of the center area.
    self.tree_view = ZScalableScrolledDecisionTreeView(self, 0, 0, width/2, height)   
   
    self.add(self.text_editor)
    self.add(self.tabbed_window)
       
    self.tabbed_window.add("Description",     self.description)
    self.tabbed_window.add("ConfusionMatrix", self.figure_view)
    self.tabbed_window.add("DecisionTree",    self.tree_view)
    
    self.figure_view.hide()
    self.tree_view.hide()
    
    self.show()
    
  def add_datasets_combobox(self):
    self.dataset_id = Iris
    self.datasets_combobox = ZLabeledComboBox(self, "Datasets", Qt.Horizontal)
    
    # We use the following datasets of sklearn to test DecisionTreeClassifier.
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
    self.model = DecisionTreeClassifierModel(self.dataset_id, self)
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
    self.tree_view.hide()
    if plt.gcf() != None:  
      plt.close()
    
  def visualize(self, cmatrix, tree):
    # 1 Show figure view
    self.figure_view.show()
    if plt.gcf() != None:
      plt.close()

    sns.set()
    df = pd.DataFrame(cmatrix)
    sns.heatmap(df, annot=True, fmt="d")
    
    self.figure_view.set_figure(plt)

    # 2 Show tree view
    self.tree_view.show()
    
    feature_names = None
    try:
      feature_names = tree.dataset.feature_names
    except:
      pass
      
    target_names  = None
    try:
      target_names = tree.dataset.target_names
    except:
      pass  
      
    self.tree_view.set_tree(tree, feature_names, target_names)
   

############################################################
#    
if main(__name__):

  try:
    app_name  = os.path.basename(sys.argv[0])
    applet    = QApplication(sys.argv)
  
    main_view = MainView(app_name, 40, 40, 1000, 500)
    main_view.show ()

    applet.exec_()

  except:
    traceback.print_exc()
    
