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

# 2018/09/20

# ZThreadingMixInUDPServer.py

# encoding utf-8

# Simple UDPServer example to accept single UDPClien
# See https://docs.python.org/3/library/socketserver.html
# See also: https://gist.github.com/arthurafarias/7258a2b83433dfda013f1954aaecd50a#file-server-py

import os
import sys
import time

import socketserver
import threading
import traceback

from SOL4Py.ZSingleton import *

##################################################
#
class ZThreadingMixInUDPServer(ZSingleton):
  
  # Inner classes start.
  # Default RequestHandler
  class _UDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
      print(self.__class__.__name__ + self.handle.__name__ + " start")
      print("Curent thread name:{}".format(threading.current_thread().name))
      try:
        while True:
          bytes = self.rfile.readline().strip() 
          if len(bytes) == 0:
            break
          ZSingleton.get_instance().request_handle_callback(bytes, self.wfile)

      except:
        traceback.print_exc()

  # Inner class
  class _ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass
 
  # Inner classes end.
  
 
  ##
  # Constructor
   
  def __init__(self, ipaddress, port, request_handler_class=None):
    self.ipaddres      = ipaddress
    self.port          = port

    ZSingleton.set_instance(self)
    
    if request_handler_class == None:
      # Register the default request handler.
      self.server        = self._ThreadedUDPServer((ipaddress, port), 
                                  self._UDPRequestHandler)
    else:
      self.server        = self._ThreadedUDPServer((ipaddress, port), 
                                  request_handler_class)
                                  
    self.server.allow_reuse_address = True
 
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True


  # Please redefine your own method 'request_handle_callback' in a subclass derived from this class.
  def request_handle_callback(self, bytes, writer):
    text = bytes.decode("utf-8")
    import datetime
    now = datetime.datetime.now()
    print("Recieved at {} data :{}".format(now, text)) 
    reply  = "OK"
    breply = reply.encode("utf-8")
    writer.write(breply)


  def start(self):
    print(self.__class__.__name__ + "::" + self.start.__name__ + "start")
    self.server_thread.start()


  def close(self):
    self.server.shutdown()
    print("sever shutdown")
    self.server.server_close()
    print("server close")

