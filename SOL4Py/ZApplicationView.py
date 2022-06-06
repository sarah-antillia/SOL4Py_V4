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

#  ZApplicationView.py

# encoding: utf-8

import sys
import os
import traceback

from SOL4Py.ZMain               import main, formatted_traceback
from SOL4Py.ZVerticalPane       import ZVerticalPane

from SOL4Py.ZHorizontalLayouter import ZHorizontalLayouter
from SOL4Py.ZVerticalLayouter   import ZVerticalLayouter
from SOL4Py.ZGridLayouter       import ZGridLayouter

from PyQt5 import QtCore, QtWidgets, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
 
class Z:
  Horizontal = 0
  Vertical   = 1
  Grid       = 2
  

class ZApplicationView(QMainWindow):
  
  # Constructor
  def __init__(self, title, x, y, width, height, layout=Z.Horizontal):
    QMainWindow.__init__(self)
    self.terminated = False
    
    self.setGeometry(x, y, width, height)
       
    self.setAttribute(Qt.WA_DeleteOnClose)

    self.title = title
    
    self.setWindowTitle(title)
    
    self.layout = layout
    
    self.main_layouter = None
   
    if self.layout == Z.Horizontal:
      self.main_layouter = ZHorizontalLayouter(self)

    if self.layout == Z.Vertical:
      self.main_layouter = ZVerticalLayouter(self)

    if self.layout == Z.Grid:
      self.main_layouter = ZGridLayouter(self)
      
    self.add_toolbar()

    self.add_file_menu()

    self.add_edit_menu()

    self.add_help_menu()
    
    self.add_control_pane()


  def add(self,  widget, x=0, y=0):
    self.main_layouter.add_widget(widget, x, y)
    
  def reshape(self, x, y, width, height):
    self.move(x, y)
    self.resize(width, height)

  def set_filenamed_title(self, filename):
    self.setWindowTitle(filename + " - " + self.title)
    

  def get_layouter(self):
    return self.main_layouter


  def get_layout(self):
    return self.main_layouter.get_layout()


  # Please define your own add_toolbar method in a subclass derived from this class.    
  def add_toolbar(self):
    pass
  

  # Please define your own add_control_pane method in a subclass derived from this class.    
  def add_control_pane(self):
    pass

  def set_right_dock(self, widget, dockingFeature=False):
    # Add the control_pane to the right_dock_area of QMainWindow.
    
    self.right_dock = QDockWidget(None, self)
    if dockingFeature == False:
      # Disable docking features
      self.right_dock.setTitleBarWidget(QWidget(None))
      self.right_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

    self.right_pane = widget
    self.right_dock.setWidget(self.right_pane)
    self.addDockWidget(Qt.RightDockWidgetArea, self.right_dock)


  def set_top_dock(self, widget, dockingFeature=False):
    # Add the target to the top_dock_area of QMainWindow.
    
    self.top_dock = QDockWidget(None, self)
    if dockingFeature == False:
      # Disable docking features
      self.top_dock.setTitleBarWidget(QWidget(None))
      self.top_dock.setFeatures(QDockWidget.NoDockWidgetFeatures)

    self.top_pane = widget
    self.top_dock.setWidget(self.top_pane)
    self.addDockWidget(Qt.TopDockWidgetArea, self.top_dock)


  # Please define your own add_file_menu in a subclass derived from this class, if needed.    
  def add_file_menu(self):
    # Typical file menu    
    self.file_menu = QMenu('&File', self)
    self.file_menu.addAction('&New',  self.file_new)
    self.file_menu.addAction('&Open', self.file_open)
    self.file_menu.addAction('&Save', self.file_save)
    self.file_menu.addAction('&Save As', self.file_save_as)
    self.file_menu.addAction('&Quit', self.file_quit)
    self.menuBar().addMenu(self.file_menu)

  # Please define your own add_edit_menu method in a subclass derived from this class, if needed.    
  def add_edit_menu(self):
    # Typical edit menu    
    self.edit_menu = QMenu('&Edit', self)
    self.edit_menu.addAction('&Cut',   self.edit_cut)
    self.edit_menu.addAction('&Copy',  self.edit_copy)
    self.edit_menu.addAction('&Paste', self.edit_paste)
    self.menuBar().addMenu(self.edit_menu)

  # Please define your own add_help_menu in a subclass derived from this class, if needed.    
  def add_help_menu(self):
    self.help_menu = QMenu('&Help', self)
    self.menuBar().addSeparator()
    self.menuBar().addMenu(self.help_menu)
    self.help_menu.addAction('&About',   self.help_about)
    self.help_menu.addAction('&Version', self.help_version)


  def add_image(self, image, name=""):
    self.drawing_area.add_image(image, name)

  def read_image(self, filename):
    image_reader = ZOpenCVImageReader()
    return image_reader.read(filename)
  
  def set_image(self, index, image, name=""):
    self.drawing_area.set_image(index, image, name)
     
  # File menu callbacks.
  #
  def file_new(self):
    QMessageBox.information(self, "FileNew",
                    "Default file_new method, but do nothing here.")
    
  # Default file_open method to read an image file by using ZOpenCVImageReader
  # and set the image read to the first area of ZDrawingArea.
  def file_open(self):
    QMessageBox.information(self, "FileOpen",
                    "Default file_open method, but do nothing here.")

  def file_save(self):
    QMessageBox.information(self, "FileSave",
                    "Default file_save method, but do nothing here.")

  def file_save_as(self):
    QMessageBox.information(self, "FileSaveAs",
                    "Default file_saveas method, but do nothing here.")

  def file_quit(self):
    self.terminated = True
    self.close()
 

  # Edit menu callbacks.
  #
  def edit_copy(self):
    QMessageBox.information(self, "Copy", "eidt_copy: Default menu callback")
    
  def edit_cut(self):
    QMessageBox.information(self, "Cut", "eidt_cupt: Default menu callback")
 
  def edit_paste(self):
    QMessageBox.information(self, "Paste", "eidt_paste: Default menu callback")
 
  # Help menu callbacks.
  #
  def help_about(self):
    QMessageBox.about(self, "About", "OpenCVApplication: Copyright (c) 2018 Antillia.com")
    
  def help_version(self):
    QMessageBox.information(self, "Version", "SOL4Py1.0 on Python3 and PyQt5 ")

  # close Event handler 
  def closeEvent(self, ce):
    self.terminated = True
    sys.exit(0)
    
  # Define your own render method in a subclass derived from this class
  def render(self):
    pass

  def is_terminated(self):
    return self.terminated
    pass
    
  def get_title(self):
    return self.title
    
#def main(name):    
#  if name == '__main__':
#    return True
#  else:
#    return False

