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
# ZAESFileCipher.py

import traceback

from SOL4Py.crypto.ZAESCipher import *

class ZAESFileCipher(ZAESCipher):
    
    # The constructor
    def __init__(self):
        super().__init__()

    # This method will read a file, and decrypt the read data by key and iv, and save it to another file.
    # key may be any text string.
    # iv should be a binary byte array, for example Random.get_random_bytes(AES.block_size)
    def encrypt(self, in_filename, out_filename, key, iv):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb" ) as infile:
            data = infile.read()
        encrypted = super().encrypt(data, key, iv)

        with open(out_filename, "wb" ) as outfile:
            outfile.write(encrypted)


    # This method will read a file, and decrypt the read data by key and iv, and save it to another file.
    #
    # key may be any text string.
    # iv should be a binary byte array, for example Random.get_random_bytes(AES.block_size)
    def decrypt(self, in_filename, out_filename, key, iv):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb") as infile:
            data = infile.read()

        decrypted = super().decrypt(data, key, iv)

        with open(out_filename, "wb") as outfile:
            outfile.write(decrypted)


