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

# 2020/01/30
# See also https://stackoverflow.com/questions/5241031/python-inserting-and-retrieving-binary-data-into-mysql

# encoding: utf-8
0
# InsertIntoTable.py



"""
create table test.User (
  id             bigint unsigned not null primary key auto_increment,
  auth_token     varchar(40)    default NULL,          
  email          varchar(255)   unique default NULL,
  password       varchar(512)   default NULL,      #(AES IV) + (AES ENCRUPTED Password) 
  validated      bool           default False,     
  last_modified  datetime       default NOW()
);

"""


import sys
import os
import configparser

sys.path.append('../')

from SOL4Py.ZMain  import *
import base64

from SOL4Py.mysql.ZMySQLDB  import *
from SOL4Py.crypto.ZAESIVEmbeddedCipher import *
from SOL4Py.generator.ZTokenGenerator import *
from SOL4Py.generator.ZEmailAddressGenerator import *
from SOL4Py.generator.ZPasswordGenerator import *

       
if main(__name__):
  # user password database 
  # foo password  test
  
  db =  ZMySQLDB(argv=sys.argv)
  
  try:
   
    for i in range (1000):
        token_generator   = ZTokenGenerator()
        email_generator   = ZEmailAddressGenerator()
        password_generator= ZPasswordGenerator()

        atoken   = token_generator.generate(20)
        email    = email_generator.generate()
        password = password_generator.generate()
        
        key  = email
        cipher = ZAESIVEmbeddedCipher(ZCipher.AS_HEX) 
        hex_iv_password = cipher.encrypt(password, key)
                
        print("Auth_token   {}".format(atoken))
        print("Email        {}".format(email))
        
        print("Password     {}".format(password)) 
        try:
            insert = "INSERT INTO test.User (auth_token, email, password) VALUES(%s, %s, %s)"
            values = (atoken, email, hex_iv_password)
            
            db.execute(insert, values)

        except:
            traceback.print_exc()
            db.rollback()

    db.commit()
        
  except Exception as ex:
    traceback.print_exc()
    db.rollback()
      
  finally:
    db.connection.close()
 
  