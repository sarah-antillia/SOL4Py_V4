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

# ZClientRequestHandlerThread.py

# encoding:utf-8


import sys
import os
import traceback
import socket
import threading
import time

class ZClientRequestHandlerThread(threading.Thread):
  DATA_ENCODER   = "utf-8"
  BUF_SIZE       = 1024*8
  SLEEP_INTERVAL = 0.01
  
  
  ## 
  # Construcotr
  def __init__(self, client, address, server_sock):
   super(ZClientRequestHandlerThread, self).__init__()

   self.client = client
   self.address = address
   self.server_sock = server_sock
   self.looping = True 
   self.reply  = "OK"
   if ZClientRequestHandlerThread.DATA_ENCODER != None:
     self.reply = self.reply.encode(ZClientRequestHandlerThread.DATA_ENCODER)
     

   
  # Default client request handler
  # Please redefine handle_request method in a subclass derived from this class.
  #
  def handle_request(self, data):
    if ZClientRequestHandlerThread.DATA_ENCODER != None:
      data = data.decode(ZClientRequestHandlerThread.DATA_ENCODER)
    
    # Print the received data.  
    print("Recv:{}".format(data))
    
    # Send self.reply to self.client.
    self.client.send(self.reply)


  # Thread main procedure, which can be called by thread.start()
  def run(self):
    print("Thread run:: start") 
    print("Connected from: {} {}".format(self.client, self.address))

    while self.looping:
      try:
        time.sleep(ZClientRequestHandlerThread.SLEEP_INTERVAL)
        data = self.client.recv(ZClientRequestHandlerThread.BUF_SIZE)
        if len(data):
          self.handle_request(data)
        else:
          raise Exception("Disconnected from: {} {}".format(self.client, self.address))

      except (BlockingIOError, socket.error):
        continue

      except (KeyboardInterrupt, SystemExit):
        print("Caught KeyboardIntrrupt exception")
        break
 
      except:
        traceback.print_exc()
        break
    
    self.stop()


  def stop(self):
    try:
    
      self.client.shutdown(socket.SHUT_RDWR)
      self.client.close()
    except:
      pass
