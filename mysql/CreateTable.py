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

# CreateTable.py

# 2020/01/30

import sys
import os
import configparser

sys.path.append('../')

from SOL4Py.ZMain  import *

from SOL4Py.mysql.ZMySQLDB  import *

"""
create table test.User (
  id             bigint unsigned not null primary key auto_increment,
  auth_token     varchar(40)    default NULL,          
  email          varchar(255)   unique default NULL,
  password       varchar(512)   default NULL,     #AES ENCRUPTED Password 
  validated      bool           default False,     
  last_modified  datetime       default NOW()
);

"""
if main(__name__):
  # Commandline parameters user password dabase
      
  db = ZMySQLDB(argv=sys.argv)
  try:
    #Create test database.
    create_db  = "CREATE DATABASE IF NOT EXISTS test"
    db.execute(create_db)

    #Create test.User table

    create_tbl = "CREATE TABLE IF NOT EXISTS test.User ( "\
                 + " id             bigint unsigned not null primary key auto_increment, "\
                 + " auth_token     varchar(40)    default NULL, "\
                 + " email          varchar(255)   unique default NULL, "\
                 + " password       varchar(512) default NULL, "\
                 + " last_modified  datetime       default NOW() "\
                 + " ); "
    
    db.execute(create_tbl)
    db.commit()
    print("Created test.user Table")
             
        
  except Exception as ex:
    print("Exception {}".format(ex))

  finally:
    db.connection.close()

  