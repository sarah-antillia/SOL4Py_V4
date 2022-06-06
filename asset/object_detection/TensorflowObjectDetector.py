##
#
# This is based on Tensorflow Object Detection API
# https://github.com/tensorflow/models
#    research/object_detection/object_detection_tutorial.ipynb

import numpy as np
import os
#import six.moves.urllib as urllib
import sys
#import tarfile
import tensorflow as tf
#import zipfile

import traceback

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

from utils import label_map_util
from utils import visualization_utils as vis_util

from CocoModelDownloader import CocoModelDownloader




class TensorflowObjectDetector:

  def __init__(self, frozen_graph, labels):
    """
    frozen_graph: 
           Path to frozen detection graph. This is the actual model that is used for the object detection.  
           PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'  
    """

    self.frozen_graph = frozen_graph
    
    self.labels = labels
    
    #Load a (frozen) Tensorflow model into memory.
    
    detection_graph = tf.Graph()

    with detection_graph.as_default():
      od_graph_def = tf.GraphDef()
      with tf.gfile.GFile(self.frozen_graph, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')
    
    #Loading label map
    #Label maps map indices to category names, so that when our convolution network predicts 5, 
    
    self.category_index = label_map_util.create_category_index_from_labelmap(
              self.labels, use_display_name=True)

    self.NUM_DETECTIONS    = 'num_detections'
    self.DETECTION_CLASSES = 'detection_classes'
    self.DETECTION_BOXES   = 'detection_boxes'
    self.DETECTION_MASKS   = 'detection_masks'
    self.DETECTION_SCORES  = 'detection_scores'


  def load_image_into_numpy_array(self, image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

  #2020/06/20
  # Detect objectes in each image in input_image_dir, and save the detected image 
  # to output_image_dir.
    
  def detect_all(self, input_image_dir, output_image_dir):
      if not os.path.exists(input_image_dir):
          raise Exception("Not found input_image_dir {}".format(input_image_dir))

      output_image_dir = os.path.join(os.getcwd(), output_image_dir)
      if not os.path.exists(output_image_dir):
          os.makedirs(output_image_dir)
      
      image_list = []

      if os.path.isdir(input_image_dir):
        image_list.extend(glob.glob(os.path.join(input_image_dir, "*.png")) )
        image_list.extend(glob.glob(os.path.join(input_image_dir, "*.jpg")) )

      print("image_list {}".format(image_list) )
          
      for image_filename in image_list:
          #image_filename will take images/foo.png
          image_file_path = os.path.abspath(image_filename)
          
          print("filename {}".format(image_file_path))
          
          image_np, output_dict = self.detect(image_file_path, output_image_dir)
 
          detected_image = Image.open(out_image_file) 

          fname = self.get_filename_only(image_file_path)            
          output_image_filename = os.path.join(output_image_dir, fname)

          detected_image.save(output_image_filename)

          print("output_image_filename {}".format(output_image_filename))
          
    
  
  ## Object detection a single image to image_path
  
  def detect(self, image_path, image_output_dir):
    image = Image.open(image_path)
    
    # the array based representation of the image will be used later in order to prepare the
    # result image with boxes and labels on it.
    
    image_np = self.load_image_into_numpy_array(image)
    
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]   
    image_np_expanded = np.expand_dims(image_np, axis=0)
    
    # Actual detection.
    #output_dict = run_inference_for_single_image(image_np, detection_graph)
        
    with self.frozen_graph.as_default():
      with tf.Session() as sess:
      
        # Get handles to input and output tensors
        ops = tf.get_default_graph().get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in [
            self.NUM_DETECTIONS,
            self.DETECTION_CLASSES,
            self.DETECTION_BOXES,
            self.DETECTION_MASKS,
            self.DETECTION_SCORES,
        ]:
          tensor_name = key + ':0'
        
          if tensor_name in all_tensor_names:
            tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                tensor_name)

        if self.DETECTION_MASKS in tensor_dict:
          # The following processing is only for single image
          detection_boxes = tf.squeeze(tensor_dict[self.DETECTION_BOXES], [0])
          detection_masks = tf.squeeze(tensor_dict[self.DETECTION_MASKS], [0])
          
          # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
          real_num_detection = tf.cast(tensor_dict[self.NUM_DETECTIONS][0], tf.int32)
          
          detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
          
          detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
          
          detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
              detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])
          
          detection_masks_reframed = tf.cast(
              tf.greater(detection_masks_reframed, 0.5), tf.uint8)
          
          # Follow the convention by adding back the batch dimension
          tensor_dict[self.DETECTION_MASKS] = tf.expand_dims(
              detection_masks_reframed, 0)
              
        image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

        # Run inference
        output_dict = sess.run(tensor_dict,
                               feed_dict={image_tensor: np.expand_dims(image_np, 0)})

        # all outputs are float32 numpy arrays, so convert types as appropriate
        output_dict[self.NUM_DETECTIONS] = int(output_dict[self.NUM_DETECTIONS][0])
        
        output_dict[self.DETECTION_CLASSES] = output_dict[self.DETECTION_CLASSES][0].astype(np.uint8)
        
        output_dict[self.DETECTION_BOXES] = output_dict[self.DETECTION_BOXES][0]
        
        output_dict[self.DETECTION_SCORES] = output_dict[self.DETECTION_SCORES][0]
        
        if self.DETECTION_MASKS in output_dict:
          output_dict[self.DETECTION_MASKS] = output_dict[self.DETECTION_MASKS][0]

    filename_only = get_filename_onl(image_path)
    
    ouput_image_filepath = os.path.joins(image_output_dir, filename_only)

    # Draw detected boxes, classes, scores onto image_np,
    # and save it to the output_image_filepath
    self.visualize(image_np, output_dict, output_image_filepath)



  def visualize(self, image_np, output_image_filepath):
  
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict[self.DETECTION_BOXES],
        output_dict[self.DETECTION_CLASSES],
        output_dict[ self.DETECTION_SCORES],
        self.category_index,
        instance_masks=output_dict.get(self.DETECTION_MASKS),
        use_normalized_coordinates=True,
        line_thickness=8)
    pil_img = Image.fromarray(image_np)

    pil_img.save(ouput_image_filepath) 

    
  def get_filename_only(self, input_image_filename):

     rpos  = input_image_filename.rfind("/")
     fname = input_image_filename

     if rpos >0:
         fname = input_image_filename[rpos+1:]
     else:
         rpos = input_image_filename.rfind("\\")
         if rpos >0:
            fname = input_image_filename[rpos+1:]
     return fname
  
  
##
#
#
if __name__ == "__main__":
  use_coco_model = true
  
  try:
     input_image_path = "images/img.png"
     output_image_dir = "detected"
     
     frozen_graph_path = ""
     labels            = ""
     if len(sys.argv) >=2:
        input_image_path = sys.argv[1]
        
     if len(sys.argv) >=3:
        frozen_graph = sys.argv[2]
     if len(sys.argv) ==4:
        label = sys.argv[3]
     
     if user_coco_model==true:
     
       downloader = CocoModelDownloader()
       downloader.download()
       frozen_graph = downloader.get_frozen_graph_path()
       label       = downloader.get_label_path()
          
     detector = TensorflowObjectDetector(frozen_graph, label)
     if os.path.exists(input_image_path):
        
       if os.path.isfile(input_image_path):
         detector.detect(input_image_path, ouput_image_dir)
       else:
         detector.detect_all(input_image_path, ouput_image_dir)
       
     
      
  except Exception as ex:
    traceback.print_exc()

