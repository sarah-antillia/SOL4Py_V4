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

# 2019/05/01

# ZEpochLogServer.py

import os
import sys
import time

import socketserver
import threading
import traceback

sys.path.append('../../')

from SOL4Py.ZMain  import *
from SOL4Py.network.ZThreadedUDPServer  import *

#=================================================
#
class ZEpochLogServer(ZThreadedUDPServer):

  ##
  # Constructor
  def __init__(self, ipaddress, port):
    ZThreadedUDPServer.__init__(self, ipaddress, port)
  
  # 
  def request_handle_callback(self, bytes, writer):
    print(__class__.__name__ + "::" + __class__.request_handle_callback.__name__ + " start")
    text = bytes.decode("utf-8")
    print(text)
    
    if "," in text:
      epoch, loss, acc, val_loss, val_acc = text.split(",")
  
      print("epoch:{} loss:{} acc:{} val_loss:{} val_acc:{}".format(epoch, loss, acc, val_loss, val_acc))
      # The values loss and acc may be plotted on figure of matplot. 


##################################################
#
#     
if main(__name__):
  ipaddress = "127.0.0.1"
  port      = 7777
  if len(sys.argv) >= 2:
    ipaddress = str(sys.argv[1])
  if len(sys.argv) >= 3:
    port = int(sys.argv[2])
    
  server = ZEpochLogServer(ipaddress, port)

  try:
    server.start()
    
    while True: 
      time.sleep(1)

  except (KeyboardInterrupt, SystemExit):
    print("Caught an exception")

  except:
    traceback.print_exc()

  else:
    pass

  finally:
    server.close()
    exit()
    