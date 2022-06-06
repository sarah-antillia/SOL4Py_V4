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

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit,QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
 
class PanedWindow(QTabWidget):        
 
    def __init__(self, parent, width, height):   
        super(PanedWindow, self).__init__(parent)
        self.layout = QVBoxLayout(self)
 
        # Initialize tab screen

 
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
 
        # Add tabs
        self.addTab(self.tab1, "Tab 1")
        self.addTab(self.tab2, "Tab 2")
 
        # Create first tab
        self.tab1.layout = QVBoxLayout(self.tab1)
        self.text_editor = QTextEdit("Hello \n World\n")
        self.tab1.layout.addWidget(self.text_editor)
 

        self.resize(width, height) 

