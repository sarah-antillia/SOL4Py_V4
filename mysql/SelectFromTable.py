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

# SelectFromTable.py


# 2020/01/30

# encoding: utf-8

"""
create table test.User (
  id             bigint unsigned not null primary key auto_increment,
  auth_token     varchar(40)    default NULL,          
  email          varchar(255)   unique default NULL,
  password       varchar(512) default NULL,      #AES ENCRUPTED Password 
  validated      bool           default False,     
  last_modified  datetime       default NOW()
);

"""


import sys
import os
import traceback
import configparser

sys.path.append('../')

from SOL4Py.ZMain  import *

from SOL4Py.mysql.ZMySQLDB  import *
from SOL4Py.crypto.ZAESIVEmbeddedCipher import *

       
if main(__name__):
  # user passwd database 
  
  db = ZMySQLDB(argv=sys.argv)
   
  try:
    select = "SELECT id, auth_token, email, password FROM test.User"

    cursor = db.connection.cursor()
    cursor.execute(select)
  
    rows = cursor.fetchall()
    
    for row in rows:
      (id, auth_token, email, hex_iv_password) = row
      cipher = ZAESIVEmbeddedCipher(ZCipher.AS_HEX)

      key    = email
      decrypted = cipher.decrypt(hex_iv_password, key)
      
      utf8_decrypted = decrypted.decode('utf-8')
   
      print("auth_token {}".format(auth_token))
      print("email      {}".format(email))
      print("password   {}".format(utf8_decrypted))

    cursor.close()
    
  except:
     traceback.print_exc()
     
  finally:
    db.connection.close()
 
  