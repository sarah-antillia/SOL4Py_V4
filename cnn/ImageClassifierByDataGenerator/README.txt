1. Small VegeFruits dataset

 The following folders contain a very small number of images dataset on VegeFruits.
 
  dataset\train
  dataset\valid
 
2. Please run the following command to generate a ImageModel weight file
 on the above image dataset.

  >python ImageModel.py

  ImageModel.py program generates augmented images from the above dataset by using Keras ImageDataGenerato class,
and calls fit_generator method of Keras Model, and create a weight file.
 But the above training process will consume a lot of time.
 You can also download the weight file by running the following command to save your time.
 
 >python download_weight_file.py


