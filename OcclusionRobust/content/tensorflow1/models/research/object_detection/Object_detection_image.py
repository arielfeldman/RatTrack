######## Image Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 1/15/18
# Description: 
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier uses it to perform object detection on an image.
# It draws boxes and scores around the objects of interest in the image.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## but I changed it to make it more understandable to me.

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import matplotlib; matplotlib.use('Agg')  # pylint: disable=multiple-statements
import matplotlib.pyplot as plt  # pylint: disable=g-import-not-at-top
from moviepy.video.io.bindings import mplfig_to_npimage
from pylab import *

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph'
IMAGE_NAME = '/home/james/content/tensorflow1/models/research/object_detection/images/train/000959.jpg'

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

print(PATH_TO_CKPT)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

# Path to image
#PATH_TO_IMAGE = os.path.join(CWD_PATH,IMAGE_NAME)
PATH_TO_IMAGE = IMAGE_NAME

# Number of classes the object detector can identify
NUM_CLASSES = 6

# Load the label map.
# Label maps map indices to category names, so that when our convolution
# network predicts `5`, we know that this corresponds to `king`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value
image = cv2.imread(PATH_TO_IMAGE)
image_expanded = np.expand_dims(image, axis=0)

# Perform the actual detection by running the model with the image as input
(boxes, scores, classes, num) = sess.run(
    [detection_boxes, detection_scores, detection_classes, num_detections],
    feed_dict={image_tensor: image_expanded})

#print(boxes.shape())
#print(len(np.squeeze(boxes)))
#print(classes.shape())
#print(len(np.squeeze(classes)))
#print(len(np.squeeze(scores)))
# Draw the results of the detection (aka 'visulaize the results')

leftobj = 0
rightobj = 0

im, leftobj, rightobj = vis_util.visualize_boxes_and_labels_on_image_array(
    image,
    np.squeeze(boxes),
    np.squeeze(classes).astype(np.int32),
    np.squeeze(scores),
    category_index,
    leftobj,
    rightobj,
    use_normalized_coordinates=True,
    line_thickness=8,
    min_score_thresh=0.80)

# def barplot(leftobj, rightobj):
#     bar_width = 0.1
    # plt.bar(np.arange(2), [leftobj, rightobj], bar_width, color='blue', align='center', alpha=0.6)
    # plt.xticks(np.arange(2),("Left Object", "Right Object"))
#     # plt.show()
# fig = barplot(leftobj, rightobj)
# image[:gh,w-gw:,:] = mplfig_to_npimage(fig)
h,w,_ = image.shape
fig, ax = subplots(figsize=(4,3), facecolor='w')
# print(image[:,:,0].shape)
B = image[:,:,0].sum(axis=0)
# print('B:',B.shape)
# line, = ax.plot(B, lw=3)
plt.bar(np.arange(2), [leftobj, rightobj], 0.1, color='blue', align='center', alpha=0.6)
plt.xticks(np.arange(2),("Left Object", "Right Object"))
# print('line:',line)
# xlim([0,w])
# ylim([40000, 130000])  # setup wide enough range here
box('off')
tight_layout()

graphRGB = mplfig_to_npimage(fig)
gh, gw, _ = graphRGB.shape

# B = image[:,:,0].sum(axis=0)
# line.set_ydata(B)
image[:gh,w-gw:,:] = mplfig_to_npimage(fig)

# print(leftobj)
# All the results have been drawn on image. Now display the image.
cv2.imshow('Object detector', image)

# Press any key to close the image
cv2.waitKey(0)

# Clean up
cv2.destroyAllWindows()
