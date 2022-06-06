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

# ZMySQLDB.py

# 2020/01/30

# encoding: utf-8

# pip install mysql-connector-python

import sys
import os
import configparser

import mysql

import mysql.connector

class ZMySQLDB:
  
  ## Constructor
  def __init__(self, user=None, password=None, database=None, server='localhost', port='1521', argv=None):
    self.user = user
    self.password = password
    self.database = database

    self.host  = server
    self.port    = port
    self.cursor  = None
    self.connection = None
    if argv != None:
      #print(len(sys.argv))
      
      if len(sys.argv) <3:
        raise Exception("Usage: {} user password database [server port]")
        
      self.user     = sys.argv[1]
      self.password = sys.argv[2]
      self.database = sys.argv[3]
      self.server   = server
      self.port     = '3306',

    if len(sys.argv) > 4:
      self.server = sys.argv[4]
      
    if len(sys.argv) > 5:
      self.port   = sys.argv[5]

    self.connect()

  ## Destructor
  def __del__(self):
    try:
      if self.connection  != None:
        self.connection.close()
        self.connection = None
    except:
      pass


  def connect(self):
    self.connection = mysql.connector.connect(user=self.user, 
                                        password=self.password, 
                                        host=self.host, 
                                        database=self.database)
 
    return self.connection
 

  def query(self, sql):
    try:
       self.cursor = self.connection.cursor()
       
       self.cursor.execute(sql)
       rows = self.cursor.fetchall()
       return rows

    except Exception as ex:
       raise ex

  def execute(self, sql, values=None):
    try:
       self.cursor = self.connection.cursor()
       self.cursor.execute(sql, values)
       
    except Exception as ex:
       raise ex

  def execute_fetchone(self, sql, values=None):
    try:
       self.cursor = self.connection.cursor()
       self.cursor.execute(sql, values)
       return self.cursor.fetchone()
       
    except Exception as ex:
       raise ex
       
  def execute_fetchall(self, sql, values=None):
    try:
       self.cursor = self.connection.cursor()
       self.cursor.execute(sql, values)
       return self.cursor.fetchall()
       
    except Exception as ex:
       raise ex


  def commit(self):
    self.connection.commit()


  def rollback(self):
    self.connection.rollback()


  def get_connection(self):
    return self.connection


  def get_cursor(self):
    return self.connection.cursor()


def qt(string):
    return "`" + string + "`"


  