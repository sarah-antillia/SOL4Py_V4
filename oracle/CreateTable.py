﻿# Copyright 2020-2021 antillia.com Toshiyuki Arai
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

# 2018/09/30

import sys
import os
import configparser

sys.path.append('../')

from SOL4Py.ZMain  import *

from SOL4Py.oracle.ZOracleDB  import *

       
if main(__name__):
  # user passwd service server port    
  try:
    db = ZOracleDB(argv=sys.argv)

    create_tbl = "Create Table ZUser("\
                 + "ID Number(6) not NULL primary key,"\
                 + "Name varchar2(255) not NULL,"\
                 + "Sex  varchar2(10),"\
                 + "Age  Number(4),"\
                 + "Birthday Date,"\
                 + "Email varchar2(255),"\
                 + "Telephone varchar2(128),"\
                 + "Address varchar2(255),"\
                 + "Company varchar2(255))"
 
    db.execute(create_tbl)

  except (cx_Oracle.DatabaseError) as ex:
    print("Exception {}".format(ex))

  