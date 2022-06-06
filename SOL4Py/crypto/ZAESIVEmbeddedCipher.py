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

# 2020/01/20
# ZAESIVEmbeddedCipher.py

# encoding: utf-8
import json

from SOL4Py.crypto.ZAESCipher import *

class ZAESIVEmbeddedCipher(ZAESCipher):

    # The constructor
    def __init__(self, format=ZCipher.AS_BINARY):
        super().__init__()
        self.format = ZCipher.AS_BINARY
        
        if (format == ZCipher.AS_BINARY) or \
           (format == ZCipher.AS_HEX)    or \
           (format == ZCipher.AS_BASE64) or \
           (format == ZCipher.AS_JSON):
           
           self.format = format         
        else:
            raise Exception("ZAESIVEmbeddedCipher: Invalid format")


    # This method will encrypt raw data(str or bytes)  by key and iv.
    # key may be any text string.
    #
    # The initial vector(iv) will be generated automatically.
    # and it will be added to the encrypted data as a prefix.
    def encrypt(self, raw, key):
        # Generate iv 
        iv = Random.get_random_bytes(AES.block_size)
        encrypted = super().encrypt(raw, key, iv)
        iv_encrypted = iv + encrypted

        if self.format == ZCipher.AS_HEX:
            hex_iv_password = self.hex(iv_encrypted)
            return hex_iv_password

        elif self.format == ZCipher.AS_BASE64:
            b64_iv_encrypted = self.b64encode(iv_encrypted)
            return b64_iv_encrypted

        elif self.format == ZCipher.AS_JSON:
            b64_iv        = self.b64encode(iv).    decode('utf-8')
            b64_encrypted = self.b64encode(encrypted).decode('utf-8')
            jsonified     = json.dumps({'iv':b64_iv, 'encrypted':b64_encrypted})
            return jsonified

        elif self.format == ZCipher.AS_BINARY:
            return iv_encrypted


    # This method will decrypt encrypted data  by key and iv.
    def decrypt(self, encrypted, key):
        if self.format == ZCipher.AS_HEX:
           encrypted = self.unhex(encrypted)
           iv        = encrypted[:AES.block_size]
           enc_data  = encrypted[AES.block_size:]

        elif self.format == ZCipher.AS_BASE64:
           encrypted = self.b64decode(encrypted)
           iv        = encrypted[:AES.block_size]
           enc_data  = encrypted[AES.block_size:]
        
        elif self.format == ZCipher.AS_JSON:
            b64      = json.loads(encrypted)
            iv       = self.b64decode(b64['iv'])
            enc_data = self.b64decode(b64['encrypted'])

        elif self.format == ZCipher.AS_BINARY:
           iv       = encrypted[:AES.block_size]
           enc_data = encrypted[AES.block_size:]

        decrypted = super().decrypt(enc_data, key, iv)
        return decrypted

