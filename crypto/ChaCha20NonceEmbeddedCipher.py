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

from  SOL4Py.crypto.ZChaCha20NonceEmbeddedCipher import *


if __name__ == '__main__':
    try:
        cipher = ZChaCha20NonceEmbeddedCipher(ZCipher.AS_HEX)
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)
                
        text = 'Antarctica will contribute about a foot of sea-level rise by 2100.'
        
        encrypted = cipher.encrypt(text, key)
        decrypted = cipher.decrypt(encrypted, key)
        
        decrypted = decrypted.decode('utf-8')
        print("AS_HEX format")
        print("Text:         '{}'".format(text))
        print("TextDecrypted:'{}'".format(decrypted))
        print("are same? {}".format(text==decrypted))
        print("")

        cipher = ZChaCha20NonceEmbeddedCipher(ZCipher.AS_BASE64)
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)
        btext = b'The global warming is real. Welcome to TOKYO2020 in the hottest summer of Japan.'
        
        encrypted = cipher.encrypt(btext, key)
        decrypted = cipher.decrypt(encrypted, key)

        print("AS_BASE64 format...")
        
        print("Bytes:         '{}'".format(btext))
        print("DecryptedBytes:'{}'".format(decrypted))
        print("are same? {}".format(btext==decrypted))
        print("")

        cipher = ZChaCha20NonceEmbeddedCipher(ZCipher.AS_JSON)
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)

        btext = b'The global warming is real. Welcome to TOKYO2020 in the hottest summer of Japan.'
        
        encrypted = cipher.encrypt(btext, key)
        decrypted = cipher.decrypt(encrypted, key)
 
        print("AS_JSON format...")
        print("Bytes:         '{}'".format(btext))
        print("DecryptedBytes:'{}'".format(decrypted))
        print("are same? {}".format(btext==decrypted))
        print("")

        cipher = ZChaCha20NonceEmbeddedCipher(ZCipher.AS_BINARY)
        key   = Random.get_random_bytes(ZChaCha20Cipher.KEY_SIZE)

        btext = b'The global warming is real. Welcome to TOKYO2020 in the hottest summer of Japan.'
        
        encrypted = cipher.encrypt(btext, key)
        decrypted = cipher.decrypt(encrypted, key)
 
        print("AS_BINARY format...")
        print("Bytes:         '{}'".format(btext))
        print("DecryptedBytes:'{}'".format(decrypted))
        print("are same? {}".format(btext==decrypted))

    except:
        traceback.print_exc()
    


