class FrozenGraphLabels:

  # Constructor
  def __init__(self, frozen_graph , labels):
    # Path to frozen detection graph. This is the actual model that is used for the object detection.  

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
    #we know that this corresponds to airplane. 
    #Here we use internal utility functions, but anything that returns a dictionary mapping 
    #integers to appropriate string labels would be fine

    self.category_index = label_map_util.create_category_index_from_labelmap(
              self.labels, use_display_name=True)

