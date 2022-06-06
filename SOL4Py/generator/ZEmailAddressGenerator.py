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

# encoding: utf-8

# 2020/01/30

# This is NOT using yield.

import sys
import secrets
import numpy as np
import string

sys.path.append('../')

from SOL4Py.generator.ZGenerator import ZGenerator


###
#---------------------------------------------------------  
class ZEmailAddressGenerator(ZGenerator):
  ##
  # Constructor
  def __init__(self):
    pass


  def generate(self):
    alpabet = string.ascii_lowercase
    letters = string.ascii_lowercase + string.digits
    
    fname   = ''.join(secrets.choice(letters) for i in range(8) )
    
    sname   = ''.join(secrets.choice(letters) for i in range(6) )
    
    company = ''.join(secrets.choice(alpabet) for i in range(8) )
    
    domains = ["com", "net","org", "biz", "info", "gov", "us", "jp", "fr", "uk", "ca"]
    
    dindex = np.random.randint(0, len(domains)) 
    domain = domains[dindex]
    email =  fname + "." + sname + "@" + company + "." + domain
    return email


