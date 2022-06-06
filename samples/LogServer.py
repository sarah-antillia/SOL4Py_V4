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

# 2019/05/17

# LogServer.py

import os
import sys
import time

import socketserver
import threading
import traceback
import socketserver
import threading
import traceback

sys.path.append('../')

from SOL4Py.ZMain  import *
from SOL4Py.network.ZThreadedUDPServer  import *

#=================================================
#
class LogServer(ZThreadedUDPServer):

  ##
  # Constructor
  def __init__(self, ipaddress, port):
    ZThreadedUDPServer.__init__(self, ipaddress, port)

  # 
  def request_handle_callback(self, bytes, writer):
    text = bytes.decode("utf-8")
    print(text)



##################################################
#
#     
if main(__name__):
  ipaddress = "127.0.0.1"
  port      = 5555
  if len(sys.argv) >= 2:
    ipaddress = str(sys.argv[1])
  if len(sys.argv) >= 3:
    port = int(sys.argv[2])
 
  print("ipaddress: {} port:{}".format(ipaddress, port))
     
  server = LogServer(ipaddress, port)

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
    