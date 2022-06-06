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
# ZAESFileBatchCipher.py

import traceback

from SOL4Py.crypto.ZAESFileCipher import *

class ZAESFileBatchCipher(ZAESCipher):

    # encrpted file format: iv + real_encrypted_data

    # The constructor
    def __init__(self):
        super().__init__()

    # This method will read a file into a memory in a lump, and decrypt the read data by key and iv, 
    # and save it to another file.
    # key may be any text string.
    # iv is generated automaticall in this method, and embedded to the ecnrypted file as something like this:
    # iv + real_encrypted__data
    def encrypt(self, in_filename, out_filename, key):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb" ) as infile:
            data = infile.read()
        # Generate iv 
        iv = Random.get_random_bytes(AES.block_size)
        encrypted = super().encrypt(data, key, iv)
        iv_encrypted = iv + encrypted
        with open(out_filename, "wb" ) as outfile:
            outfile.write(iv_encrypted)
      
 
    # This method will read a file into a memory in a lump, and decrypt the read data by key and iv, 
    # and save it to another file.
    #
    # key may be any text string.
    # iv is read from the input file.
    def decrypt(self, in_filename, out_filename, key):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb") as infile:
            encrypted = infile.read()

        # Extract iv from the encrpted bytes.
        iv = encrypted[:AES.block_size]
        # Extrat the real encrypted data from the encrypted
        encrypted = encrypted[AES.block_size:]

        decrypted = super().decrypt(encrypted, key, iv)

        with open(out_filename, "wb") as outfile:
            outfile.write(decrypted)

