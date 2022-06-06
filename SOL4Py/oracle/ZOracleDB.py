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

# OracleDB.py

# 2018/09/30

# encoding: utf-8

import sys
import os
import configparser

import cx_Oracle

class ZOracleDB:

  def __init__(self, user=None, passwd=None, service=None, server='localhost', port='1521', argv=None):
    self.user = user
    self.passwd = passwd
    self.service = service
    self.server  = server
    self.port    = port
    self.cursor  = None
    self.connection = None
    if argv != None:
      if len(sys.argv) <=3:
        raise Exception("Usage: {} user passwd service [server port]")
        
      self.user    = sys.argv[1]
      self.passwd  = sys.argv[2]
      self.service = sys.argv[3]
      self.server  = 'localhost'
      self.port    = '1521'
    
    if len(sys.argv) > 4:
      self.server = sys.argv[4]
      
    if len(sys.argv) > 5:
      self.port   = sys.argv[5]

    self.connect()
    
  def connect(self):
    try:
      self.connection = cx_Oracle.connect(self.user, self.passwd, 
                     self.server + ':' + self.port + '/' + self.service )
      self.cursor = self.connection.cursor()

    except (cx_Oracle.DatabaseError) as ex:
      print(ex)
      raise ex

  def query(self, sql):
    try:
       self.cursor.execute(sql)
       rows = self.cursor.fetchall()
       return rows

    except (cx_Oracle.DatabaseError) as ex:
       print(ex)
       raise ex

  def execute(self, sql):
    try:
       self.cursor.execute(sql)

    except (cx_Oracle.DatabaseError) as ex:
       print(ex)
       raise ex


  def get_connection(self):
    return self.connection


  def get_cursor(self):
    return self.cursor


  