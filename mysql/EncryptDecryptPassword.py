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
# See https://bugs.mysql.com/bug.php?id=79317

# See also https://stackoverflow.com/questions/5241031/python-inserting-and-retrieving-binary-data-into-mysql

# encoding: utf-8

# EncryptDecryptPassword.py


# As reported on the web-site: https://bugs.mysql.com/bug.php?id=79317,
# the binary columns in a table of MySQL may cause an unexpected warning something like
#
#  Warning, NNNNNN, Invalid utf8 character string: 'xxxxxxx'
#
# To avoid this problem, it's much better to use varchar instead of binary to the columns.

# So we define the following test.User talbe, where password to be varchar not binary.
# By using ZAESIVEmbeddeCipher class, we encrypt a password and get a hex-formatted iv_embeddede_encrypted_password
# and insert the hex-formated string to the varchar password column of the test.User table.
# Of course, MySQL has a own AES_ENCRYPT and AES_DECRYPT functions, but those are MySQL specific features,
# not available in other Database systems.

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


if main(__name__):
  # user password database 
  # foo password  test

  try:
    db =  ZMySQLDB(argv=sys.argv)
    MAGIC    = '&=~|%asZpo()/?moon'
    email    = 'darkside.1991@xstarnet.mars'
    password = "1991=~Zpo()#$%/?moon"
    print("Email        {}".format(email))
            
    print("Password     {}".format(password)) 

    try:
        print("Select ...")
        select = "SELECT auth_token, email, password FROM test.User WHERE email=%s LIMIT 1"
        values = (email, )

        row =db.execute_fetchone(select, values)
        if row ==None:
            print("Not registered yet in test.User table, try to insert a record for email={}".format(email))
            token_generator   = ZTokenGenerator()

            atoken   = token_generator.generate(20)
            key      = email  + MAGIC

            
            cipher = ZAESIVEmbeddedCipher(ZCipher.AS_HEX) 
            hex_iv_password = cipher.encrypt(password, key)
                    
            print("Auth_token   {}".format(atoken))
            print("Hex_iv_password {}".format(hex_iv_password))

            print("Insert ...")
            
            insert = "INSERT INTO test.User (auth_token, email, password) VALUES(%s, %s, %s)"
            values = (atoken, email, hex_iv_password)
            
            db.execute(insert, values)
            db.commit()
        else:
           print("Already inserted email {}".format(email))
           
    except:
        pass
        #traceback.print_exc()
        #db.rollback()

    try:
        print("Select ...")
        select = "SELECT auth_token, email, password FROM test.User WHERE email=%s LIMIT 1"
        values = (email, )

        row =db.execute_fetchone(select, values)
        if row != None:
           (auth_token, email, hex_iv_password) = row 

           print("autoken {}".format(auth_token))

           print("email {}".format(email))
           
           print("hex_iv_password {}".format(hex_iv_password))

           cipher = ZAESIVEmbeddedCipher(ZCipher.AS_HEX) 
           key = email + MAGIC
           decrypted = cipher.decrypt(hex_iv_password, key)
           utf8_decrypted = decrypted.decode('utf-8')
           print("Decrypted password {}".format(utf8_decrypted))               
           if password == utf8_decrypted:
              print("...Password decrypted correctly")
    except:
        traceback.print_exc()

  
  except Exception as ex:
      traceback.print_exc()
      db.rollback()
      
  finally:
      db.connection.close()
 
  