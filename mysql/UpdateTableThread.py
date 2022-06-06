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
# UpdateTableThread.py



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
from SOL4Py.mysql.ZThreadedMySQLConnection  import *
from SOL4Py.crypto.ZAESIVEmbeddedCipher import *
from SOL4Py.generator.ZTokenGenerator import *
from SOL4Py.generator.ZEmailAddressGenerator import *
from SOL4Py.generator.ZPasswordGenerator import *


# Define your own thread class derived from ZThreadedMySQLConnection.

class UpdateTableThread(ZThreadedMySQLConnection):
  def __init__(self, connection):
    super().__init__(connection)

  # Define your own thread procedure 
  def run(self):
    try:
      self.cursor.execute("SELECT id, email  FROM test.User WHERE email LIKE '%.com'")
      rows = self.cursor.fetchall()

      for row in rows:
          (id, email) = row
          print("Hit record: id {} email {}".format(id, email))
          
          token_generator    = ZTokenGenerator()
          password_generator = ZPasswordGenerator()

          new_atoken   = token_generator.generate(20)
          new_password = password_generator.generate()

          key  = email
          cipher = ZAESIVEmbeddedCipher(ZCipher.AS_HEX) 
          new_hex_iv_password = cipher.encrypt(new_password, key)

          print("New Auth_token   {}".format(new_atoken))
          print("New Password     {}".format(new_password))
     
          update = "UPDATE test.User SET auth_token=%s, password =%s WHERE id =%s"
          values = (new_atoken, new_hex_iv_password, id)
          
          self.cursor.execute(update, values)
      
      self.commit()
              
    except:
       traceback.print_exc()
       self.rollback()


if main(__name__):
  # user password database 
  
  db = ZMySQLDB(argv=sys.argv)
   
  try:
    update_thread = UpdateTableThread(db.connection)
    update_thread.start()
    update_thread.join()
 
  except:
     traceback.print_exc()
  
  finally:
    db.connection.close()
 
  
  