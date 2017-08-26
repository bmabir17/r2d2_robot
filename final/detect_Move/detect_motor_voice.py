# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/

This file has been modified by Sam Abrahams to print out basic run-time
information. These modifications have been surrounded with the comments:
"MODIFICATION BY SAM ABRAHAMS" and "END OF MODIFICATION"
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
import sys
import tarfile

# MODIFICATION BY SAM ABRAHAMS
import time
# END OF MODIFICATION

import numpy as np
from six.moves import urllib
import tensorflow as tf
import picamera
from time import sleep
from PIL import Image

import pyttsx
from gtts import gTTS
import os

# libraries to send data to Serial port
import serial
import struct

camera = picamera.PiCamera()
# camera.resolution = (320,240)
cmd_file=open('command.txt','r+')
FLAGS = tf.app.flags.FLAGS

#define serial port
usbport = '/dev/ttyACM0'
serialArduino = serial.Serial(usbport, 9600, timeout=1)


# classify_image_graph_def.pb:
#   Binary representation of the GraphDef protocol buffer.
# imagenet_synset_to_human_label_map.txt:
#   Map from synset ID to a human readable string.
# imagenet_2012_challenge_label_map_proto.pbtxt:
#   Text representation of a protocol buffer mapping a label to synset ID.
tf.app.flags.DEFINE_string(
    'model_dir', 'model',
    """Path to classify_image_graph_def.pb, """
    """imagenet_synset_to_human_label_map.txt, and """
    """imagenet_2012_challenge_label_map_proto.pbtxt.""")
tf.app.flags.DEFINE_string('image_file', '',
                           """Absolute path to image file.""")
tf.app.flags.DEFINE_integer('num_top_predictions', 1,
                            """Display this many predictions.""")
# MODIFICATION BY SAM ABRAHAMS
tf.app.flags.DEFINE_integer('warmup_runs', 1,
                            "Number of times to run Session before starting test")
tf.app.flags.DEFINE_integer('num_runs', 1,
                            "Number of sample runs to collect benchmark statistics")
# END OF MODIFICATION

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# pylint: enable=line-too-long


class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.

    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.

    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

def warmUp(sess,softmax_tensor,image_data,start_time,graph_time):
  # MODIFICATION BY SAM ABRAHAMS
    for i in range(FLAGS.warmup_runs):
      predictions = sess.run(softmax_tensor,
                             {'DecodeJpeg/contents:0': image_data})
    runs = []
    for i in range(FLAGS.num_runs):
      start_time = time.time()
      predictions = sess.run(softmax_tensor,
                             {'DecodeJpeg/contents:0': image_data})
      runs.append(time.time() - start_time)
    for i, run in enumerate(runs):
      print('Run %03d:\t%0.4f seconds' % (i, run))
    print('---')
    print('Best run: %0.4f' % min(runs))
    print('Worst run: %0.4f' % max(runs))
    print('Average run: %0.4f' % float(sum(runs) / len(runs)))
    print('Build graph time: %0.4f' % graph_time)
    print('Number of warmup runs: %d' % FLAGS.warmup_runs)
    print('Number of test runs: %d' % FLAGS.num_runs)
    # END OF MODIFICATION
def gtts_call(str):
  tts = gTTS(text=str, lang='en')
  tts.save("good.mp3")
  os.system("mpg321 good.mp3")

def pyttsx_call(str):
  # use sys.argv if needed
  print ('running speech-test.py...')
  engine = pyttsx.init()
  if len(sys.argv) > 1:
    str = sys.argv[1]
  engine.say(str)
  engine.runAndWait()

def speak_call(str):
  pyttsx_call(str)
  #gtts_call(str)
def detect(sess,softmax_tensor,image_data,graph_time):
  # MODIFICATION BY BMAbir
  print("In detect")
  #gtts_call("start detecting")
  start_time = time.time()
  convertImage=Image.open(image_data)
  image_array=np.array(convertImage)[:,:,0:3] 
    
  predictions = sess.run(softmax_tensor,{'DecodeJpeg:0': image_array})  
  predictions = np.squeeze(predictions)
  
  #Creates node ID --> English string lookup.
  node_lookup = NodeLookup()
  top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
  for node_id in top_k:
          
          human_string= node_lookup.id_to_string(node_id)
          #print (human_string)
          #time.sleep(3)
          #gtts_call(human_string)
          #pyttsx_call(human_string)
          #time.sleep(3)
          score= predictions[node_id]
          print('%s (score= %.5f)' % (human_string,score))
          human_st_arr=human_string.split(',')
          print(human_st_arr[0])
          speak_call(human_st_arr[0])
           # for i in human_string:
             # var=i
             # print(var)
             # espeak.synth(var)
            # os.system ('espeak "{}"'. format(var))
  execTime=time.time() - start_time
  return human_string
  #print('Prediction Execution Time:',execTime)
  # END OF MODIFICATION

def detectPipeLine(sess,softmax_tensor,image_data,graph_time):
  # Modification by BMAbir
        print('Continueous detection')
        speak_call("I am now ready")
        while(True):
                
                #print(c)
                ## The raspi will wait for command from the client raspberry.
                ## It acts as a socket server
                ##cmd_string=cmd_file.readline() ##for testing#######Remove when in production
                #print(cmd_string)
                cmd_string="find_object"
                
                if(cmd_string=="find_object"):
                        print(cmd_string)
                        c=0
                        while(c<1):
                                ## take images for 9 times, rotating the head
                                start_det=time.time()
                                #img_name='cap'+str(c)+'.jpg'
                                speak_call("Let's Move!!")
                                #Forward Move
                                #Move body forward and stop right after 2.5 secs
                                serialArduino.write(b'w') #Body Move forward
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2.5)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                
                                #Move body left and stop right after 2.5 secs
                                serialArduino.write(b'a') #Body Move Left
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                
                                #Move body Right and stop right after 5 secs
                                serialArduino.write(b'd') #Body Move Right
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(6)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                
                                #Move body left and stop right after 2.5 secs
                                serialArduino.write(b'a') #Body Move Left
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                
                                #forward capture
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino 
                                img_name='cap_forward'+str(c)+'.jpg'
                                print(img_name)
                                camera.capture(img_name,'jpeg')
                                speak_call("In front of me there is a")

                                human_string_rt=detect(sess,softmax_tensor,img_name,graph_time)
                                #print(human_string_rt)
                                #espeak.synth(human_string_rt)
                                
                                #Move head left and stop right after 2.5 secs
                                serialArduino.write(b'l') #Head Move left
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2.5)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                #left capture
                                
                                img_name='cap_left'+str(c)+'.jpg'
                                camera.capture(img_name,'jpeg')
                                speak_call("In my Left there is a")
                                human_string_rt=detect(sess,softmax_tensor,img_name,graph_time)
                                #print(human_string_rt)
                                #espeak.synth(human_string_rt)
                                #Move head to center position and stop right after 2.5 secs
                                serialArduino.write(b'r') #Head Move right
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2.5)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino

                                #Move head right and stop right after 2.5 secs
                                serialArduino.write(b'r') #Head Move right
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2.5)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                #right capture
                                img_name='cap_right'+str(c)+'.jpg'
                                camera.capture(img_name,'jpeg')
                                speak_call("And in my Right a")
                                detect(sess,softmax_tensor,img_name,graph_time)
                                human_string_rt=detect(sess,softmax_tensor,img_name,graph_time)
                                #print(human_string_rt)
                                #espeak.synth(human_string_rt)
                                #Move head to center position and stop right after 2.5 secs
                                serialArduino.write(b'l') #Head Move left
                                serialArduino.readline()  #Read The executed Command from arduino
                                time.sleep(2.5)
                                serialArduino.write(b'x') #stop
                                serialArduino.readline()  #Read The executed Command from arduino
                                total_det=time.time()-start_det
                                c+=1
                        cmd_file.write('done')
                print("Detector is Idle")
    
    
    
  #END of MODIFICATION
  


def run_inference_on_image(image):
  """Runs inference on an image.

  Args:
    image: Image file name.

  Returns:
    Nothing
  """
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # Creates graph from saved GraphDef.
  start_time = time.time()
  create_graph()
  graph_time = time.time() - start_time

  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    speak_call("Almost there!")
    warmUp(sess,softmax_tensor,image_data,start_time, graph_time)
    speak_call("Beep-beep!!")
    detectPipeLine(sess,softmax_tensor,image_data,graph_time)
    

def maybe_download_and_extract():
  """Download and extract model tar file."""
  dest_directory = FLAGS.model_dir
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    def _progress(count, block_size, total_size):
      sys.stdout.write('\r>> Downloading %s %.1f%%' % (
          filename, float(count * block_size) / float(total_size) * 100.0))
      sys.stdout.flush()
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath,
                                             reporthook=_progress)
    print()
    statinfo = os.stat(filepath)
    print('Succesfully downloaded', filename, statinfo.st_size, 'bytes.')
  tarfile.open(filepath, 'r:gz').extractall(dest_directory)


def main(_):
  speak_call("I am R2D2, a droid created in BRAC University")
  speak_call("Please wait while i bootup")
  maybe_download_and_extract()
  image = (FLAGS.image_file if FLAGS.image_file else
           os.path.join(FLAGS.model_dir, 'cropped_panda.jpg'))
  run_inference_on_image(image)


if __name__ == '__main__':
  tf.app.run()
