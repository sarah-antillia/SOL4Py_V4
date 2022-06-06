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
# AESCipher.py

# encoding: utf-8

import base64
import traceback
import sys

sys.path.append('../')

from  SOL4Py.crypto.ZChaCha20Cipher import *


if __name__ == '__main__':
    try:
        cipher = ZChaCha20Cipher()
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)
        nonce = Random.get_random_bytes(ZChaCha20Cipher.NONCE_SIZE)
                
        text = 'Antarctica will contribute about a foot of sea-level rise by 2100.'
        
        encrypted = cipher.encrypt(text, key, nonce)
            
        decrypted = cipher.decrypt(encrypted, key, nonce)
        
        utf8_decrypted = decrypted.decode('utf-8')
        
        print("UTF8Text:     '{}'".format(text))
        print("UTF8Decrypted:'{}'".format(utf8_decrypted))
        print("")

        btext = b'The global warming is real. Welcome to TOKYO2020 in the hottest summer of Japan.'
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)
        nonce = Random.get_random_bytes(ZChaCha20Cipher.NONCE_SIZE)
        
        encrypted = cipher.encrypt(btext, key, nonce)
            
        decrypted = cipher.decrypt(encrypted, key, nonce)
        
        print("OriginalBytes: '{}'".format(btext))
        print("DecryptedBytes:'{}'".format(decrypted))
        print("")

    except:
        traceback.print_exc()
    


