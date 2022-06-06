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
# ZChaCha20Cipher.py

# encoding: utf-8

# pip install pycryptodome

# See also https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20.html

import base64
import traceback
import sys
import binascii

from Crypto import Random
from Crypto.Cipher import ChaCha20

import traceback

from SOL4Py.crypto.ZCipher import *

class ZChaCha20Cipher(object):
    
    KEY_SIZE    = 32
    NONCE_SIZE  = 12
    
    # The constructor
    def __init__(self):
        pass

        
    # This method will encrypt raw data(str or bytes)  by key and iv.
    # key may be created by Random.get_random_bytes(self.KEY_SIZE)  #32
    # nonce may be create by Random.get_random_bytes(self.NONCE_SIZE)    #12
    #   See https://tools.ietf.org/html/rfc7539
    # and pass it to this method.
    def encrypt(self, data, key, nonce):
        if type(data) is str:
           data = data.encode('utf-8')
        cipher = ChaCha20.new(key = key, nonce=nonce)
        encrypted  = cipher.encrypt(data)
        return encrypted
            
            
    # This method will decrypt encrypted data  by key.
    # key should be a key when used to encrypt data.
    # nonce should be a nonce when used to encrypt data
    def decrypt(self, encrypted, key, nonce):
        cipher = ChaCha20.new(key = key, nonce = nonce)
        decrypted = cipher.decrypt(encrypted)
        return decrypted

    def generate_nonce(self):
        return Random.get_random_bytes(self.NONCE_SIZE)
        
    def hex(self, data):
        return binascii.hexlify(data)

    def unhex(self, data):
        return binascii.unhexlify(data)

    def b64encode(self, data):
      return base64.b64encode(data)
      
    def b64decode(self, data):
      return base64.b64decode(data)

