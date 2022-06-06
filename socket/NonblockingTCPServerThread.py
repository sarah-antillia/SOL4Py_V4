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

# 2018/09/30

# Simple Nonblocking TCP Socket Server thread example
# NonblockingTCPServerThread.py


# encoding: utf-8

import os
import sys
import traceback
import socket
import threading
import time

sys.path.append('../')

from SOL4Py.ZMain                        import *
from SOL4Py.network.ZNonblockingTCPServerThread  import *


if main(__name__):

  ipaddress = "127.0.0.1"
  port      = 7777
  if len(sys.argv) >= 2:
    ipaddress = str(sys.argv[1])
  if len(sys.argv) >= 3:
    port = int(sys.argv[2])

  try:
    server = ZNonblockingTCPServerThread(ipaddress, port)

    server.start()
        
    # To accept KeyboardInterrupt, use the following while loop
    while True:
      time.sleep(1)

  except (KeyboardInterrupt, SystemExit):
    print("Caught an exception")
 
  except:
    traceback.print_exc()
 
  finally:
    server.stop()
    print("Server stopped")
    exit()
    
