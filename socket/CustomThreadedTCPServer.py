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

# CustomThreadedTCPServer.py

import os
import sys
import time

import socketserver
import threading
import traceback

sys.path.append('../')

from SOL4Py.network.ZThreadedTCPServer  import *

#=================================================
#
class CustomThreadedTCPServer(ZThreadedTCPServer):

  ##
  # Constructor
  def __init__(self, ipaddress, port):
    ZThreadedTCPServer.__init__(self, ipaddress, port)
  
  # 
  def request_handle_callback(self, bytes, writer):
    print(__class__.__name__ + "::" + __class__.request_handle_callback.__name__ + " start")
    text = bytes.decode("utf-8")
    loss, acc = text.split(":")
    print("Loss:{} Acc:{}".format(loss, acc))
    # The values loss and acc may be plotted on figure of matplot. 
    reply  = "OK"
    breply = reply.encode("utf-8")
    writer.write(breply)


##################################################
#
#     
if __name__ == "__main__":
  ipaddress = "127.0.0.1"
  port      = 7777
  if len(sys.argv) >= 2:
    ipaddress = str(sys.argv[1])
  if len(sys.argv) >= 3:
    port = int(sys.argv[2])
    
  server = CustomThreadedTCPServer(ipaddress, port)

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
    