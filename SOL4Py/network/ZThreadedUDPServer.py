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

# ZThreadedUDPServer.py

# encoding: utf-8

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
# Define UDPServer thread class, which handles a datagram request from a UDP client.
#
class ZThreadedUDPServer(threading.Thread, ZSingleton):

  #---------------------------------------------------------
  # Inner class starts. 
  # Define your subclass derived from DatagramRequestHandler
  # This is a default request handler.
  class _UDPRequestHandler(socketserver.DatagramRequestHandler):

    # Define your own handle method.
    def handle(self):
      #print(self.__class__.__name__ + self.handle.__name__ + " start")
      #print("Curent thread name:{}".format(threading.current_thread().name))
      try:
        while True:

          bytes = self.rfile.readline().strip() 
          if len(bytes) == 0:
            break

          ZSingleton.get_instance().request_handle_callback(bytes, self.wfile)

      except:
        traceback.print_exc()

  # Inner class ends.
 
 
  ##
  #
  # Constructor
  def __init__(self, ipaddress, port, request_handler_class = None):
    super(ZThreadedUDPServer, self).__init__()
    #print(self.__class__.__name__ + "::" + self.run.__name__ + " start")

    ZSingleton.set_instance(self)
        
    #print("IPAddress:{} Port:{}".format(ipaddress, port))
    self.server_address = (ipaddress, port)
    
    if request_handler_class == None:
      self.sock_server = socketserver.ThreadingUDPServer(self.server_address, self._UDPRequestHandler)
    else:
      self.sock_server = socketserver.ThreadingUDPServer(self.server_address, request_handler_class)
 
    self.sock_server.allow_reuse_address = True


  # Please redefine your own method 'request_handle_callback' in a subclass derived from this class.
  def request_handle_callback(self, bytes, writer):
    text = bytes.decode("utf-8")
    import datetime
    now = datetime.datetime.now()
    #print("Recieved at {} data :{}".format(now, text)) 
    reply  = "OK"
    breply = reply.encode("utf-8")
    writer.write(breply)

 
  # Thread main procedure.
  def run(self):
    print(self.__class__.__name__ + "::" + self.run.__name__ + " start")
    if self.sock_server != None:
      self.sock_server.serve_forever()    
    print(self.__class__.__name__ + "::" + self.run.__name__ + " end")


  # Shdown and close server_socket.
  def close(self):
    if self.sock_server != None:
      self.sock_server.shutdown() 
      print("sock_server shutdown")
       
      self.sock_server.server_close()
      print("sock_server close")


