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
# ZChaCha20NonceEmbeddedCipher.py

# encoding: utf-8

# pip install pycryptodome

# See also https://pycryptodome.readthedocs.io/en/latest/src/cipher/chacha20.html

import json
import base64
import traceback
import sys
import binascii
import traceback

from Crypto import Random
from Crypto.Cipher import ChaCha20

from SOL4Py.crypto.ZChaCha20Cipher import *

class ZChaCha20NonceEmbeddedCipher(ZChaCha20Cipher):

    # The constructor
    def __init__(self, format):
        super().__init__()
        #Default value
        self.format= ZCipher.AS_BINARY

        if (format == ZCipher.AS_BINARY) or \
           (format == ZCipher.AS_HEX)    or \
           (format == ZCipher.AS_BASE64) or \
           (format == ZCipher.AS_JSON):
           self.format = format
        else:
            raise Exception("ZChaCha20NonceEmbeddedCipher: Invalid format")

        
    # This method will encrypt raw data(str or bytes)  by key and iv.
    # key may be created by Random.get_random_bytes(self.KEY_SIZE)  #32
    # and passed to this method.
    def encrypt(self, data, key):
        #Generate a nonce byte array.
        nonce = Random.get_random_bytes(self.NONCE_SIZE)    #12
        #   See https://tools.ietf.org/html/rfc7539
        encrypted  = super().encrypt(data, key, nonce)
        
        if self.format == ZCipher.AS_HEX:
            nonce_encrypted = nonce + encrypted
            return self.hex(nonce_encrypted)
            
        elif self.format == ZCipher.AS_BASE64:
            nonce_encrypted = nonce + encrypted
            return self.b64encode(nonce_encrypted)
            
        elif self.format == ZCipher.AS_JSON:
            b64_nonce     = self.b64encode(nonce).    decode('utf-8')
            b64_encrypted = self.b64encode(encrypted).decode('utf-8')
        
            jsonified = json.dumps({'nonce':b64_nonce, 'encrypted':b64_encrypted})
            return jsonified
            
        else:
            return nonce + encrypted


    # This method will decrypt encrypted data  by key.
    # key should be a key when used to encrypt data.
    def decrypt(self, encrypted, key):
        nonce    = None
        enc_data = None
        if self.format == ZCipher.AS_HEX:
            encrypted = self.unhex(encrypted)
            nonce     = encrypted[:self.NONCE_SIZE]
            enc_data  = encrypted[ self.NONCE_SIZE:]

        elif self.format == ZCipher.AS_BASE64:
            encrypted = self.b64decode(encrypted)
            nonce     = encrypted[:self.NONCE_SIZE]
            enc_data  = encrypted[ self.NONCE_SIZE:]

        elif self.format == ZCipher.AS_JSON:
            b64      = json.loads(encrypted)
            nonce    = self.b64decode(b64['nonce'])
            enc_data = self.b64decode(b64['encrypted'])

        else:
            nonce     = encrypted[:self.NONCE_SIZE]
            enc_data  = encrypted[self.NONCE_SIZE:]

        decrypted = super().decrypt(enc_data, key, nonce)
 
        return decrypted


