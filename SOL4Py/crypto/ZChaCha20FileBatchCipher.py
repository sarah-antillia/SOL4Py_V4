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
# ZChaCha20FileBatchCipher.py

import traceback

from SOL4Py.crypto.ZChaCha20Cipher import *

class ZChaCha20FileBatchCipher(ZChaCha20Cipher):

    # encrpted file format: nonce + real_encrypted_data

    # The constructor
    def __init__(self):
        super().__init__()

    # This method will read a file into a memory in a lump, and encrypt the read data by key and nonce, 
    # and save it to another file.
    # key may be created by Random.get_random_bytes(self.KEY_SIZE)  #32
    # nonce is generated automatically in this method, and embedded to the 
    # ecnrypted file as something like this: nonce + payload
    def encrypt(self, in_filename, out_filename, key):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb" ) as infile:
            data = infile.read()
        # Generate nonce 
        nonce = self.generate_nonce()
        encrypted = super().encrypt(data, key, nonce)
        nonce_encrypted = nonce + encrypted
        with open(out_filename, "wb" ) as outfile:
            outfile.write(nonce_encrypted)
      
 
    # This method will read a file into a memory in a lump, and decrypt the read data by key and nonce, 
    # and save it to another file.
    #
    def decrypt(self, in_filename, out_filename, key):
        #This is a very simple method, but not suitable for a large file
        with open(in_filename, "rb") as infile:
            encrypted = infile.read()

        # Extract iv from the encrpted bytes.
        nonce = encrypted[:self.NONCE_SIZE]
        # Extract payload from the encrypted
        encrypted = encrypted[self.NONCE_SIZE:]
        
        decrypted = super().decrypt(encrypted, key, nonce)

        with open(out_filename, "wb") as outfile:
            outfile.write(decrypted)

