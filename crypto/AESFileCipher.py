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
# AESFileCipher.py

# encoding: utf-8

import os
import sys
import base64
import traceback
import filecmp

sys.path.append('../')

from SOL4Py.crypto.ZAESFileCipher import *


if __name__ == '__main__':
    try:
        filecipher = ZAESFileCipher()
        in_filename  = "test.txt"
        enc_filename = "enc_test.txt"
        dec_filename = "dec_test.txt"

        key = '1998key!C#$X%asZpo()/?'
        iv = Random.get_random_bytes(AES.block_size)
        
        filecipher.encrypt(in_filename, enc_filename, key, iv)

        filecipher.decrypt(enc_filename, dec_filename, key, iv)
        
        is_same = filecmp.cmp(in_filename, dec_filename)
        print('Input file:    {} {}(bytes) \nDecrypted file:{} {}(bytes)  \nare same? {}'.format(
                         in_filename,  os.path.getsize(in_filename),
                         dec_filename, os.path.getsize(dec_filename),
                         is_same))
        print("")

        key = 'key!C#$X%asZpo()tokyo2020/?'
        iv = Random.get_random_bytes(AES.block_size)
        in_filename  = "TOKYO2020.JPG"
        enc_filename = "XENC_TOKYO2020.enc"
        dec_filename = "XDEC_TOKYO2020.JPG"

        filecipher = ZAESFileCipher()

        filecipher.encrypt(in_filename, enc_filename, key, iv)
        
        filecipher.decrypt(enc_filename, dec_filename, key, iv)
        
        is_same = filecmp.cmp(in_filename, dec_filename)
        print('Input file:    {} {}(bytes) \nDecrypted file:{} {}(bytes)  \nare same? {}'.format(
                         in_filename,  os.path.getsize(in_filename),
                         dec_filename, os.path.getsize(dec_filename),
                         is_same))
        
    except:
        traceback.print_exc()
    


