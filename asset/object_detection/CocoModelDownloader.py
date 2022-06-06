# 
# # Copyright (c) 2020 Antillia.com TOSHIYUKI ARAI. ALL RIGHTS RESERVED.
#
# This is based on Tensorflow Object Detection API
# https://github.com/tensorflow/models
#    research/object_detection/object_detection_tutorial.ipynb

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

from utils import label_map_util
from utils import visualization_utils as vis_util

class CocoModelDownloader:

  def __init__(self):
    self.MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
    self.MODEL_FILE = self.MODEL_NAME + '.tar.gz'
    self.DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'


  def download(self):    
    # Download Model
    opener = urllib.request.URLopener()
    opener.retrieve(self.DOWNLOAD_BASE + self.MODEL_FILE, self.MODEL_FILE)
    tar_file = tarfile.open(self.MODEL_FILE)

    for file in tar_file.getmembers():
      file_name = os.path.basename(file.name)
      if 'frozen_inference_graph.pb' in file_name:
        tar_file.extract(file, os.getcwd())
    
    
  def get_frozen_graph_path(self):
    # self.MODEL_NAME='ssd_mobilenet_v1_coco_2017_11_17'
    # PATH_TO_FROZEN_GRAPH = self.MODEL_NAME + '/frozen_inference_graph.pb'
    path = self.MODEL_NAME + '/frozen_inference_graph.pb'
    return path


  def get_label_path(self):
    #PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
    path= os.path.join('data', 'mscoco_label_map.pbtxt')
    return path
    

