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
# ZAESFileStreamCipher.py

# See also: https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
import os
import traceback

from SOL4Py.crypto.ZAESCipher import *

class ZAESFileStreamCipher(ZAESCipher):
    # Ecrypted file format: filesize_bytes(6) +  iv(AES.block_size) + encrypted_data
    
    FILE_SIZE  = 6                #Byte size to store a size of file to be encrypted
    BYTE_ORDER = 'little'         #Byte-order specifiter 
                                  # to convert integer to bytes, and bytes to integer.
    IV_SIZE    = AES.block_size   #Byte size of AES iv(initial vector)

    FILE_BLOCK_SIZE = AES.block_size * 1024 #Byte size to be read from a file, which must be multiple of AES.block_size
    
    # The constructor
    def __init__(self):
        super().__init__()


    def encrypt(self, in_filename, out_filename, key):

        with open(in_filename, "rb" ) as infile:
            in_filesize = os.path.getsize(in_filename)

            with open(out_filename, "wb" ) as outfile:
                enc_key = SHA256.new(key.encode()).digest()
                iv = Random.get_random_bytes(AES.block_size)
                # Create AES cipher object from the enc_key and iv
                cipher = AES.new(enc_key, self.mode, iv)

                filesize = in_filesize.to_bytes(self.FILE_SIZE, self.BYTE_ORDER)

                outfile.write(filesize)
                outfile.write(iv)

                while True:
                   
                    data = infile.read(self.FILE_BLOCK_SIZE)
                    data_len = len(data)
                    if data_len == 0:
                        break
                    elif data_len % AES.block_size != 0:
                        #print("padding")
                        data = Padding.pad(data, AES.block_size, self.padding_alg)
                    #Encrypt data by cipher and write the encrypted to the outfile
                    encrypted = cipher.encrypt(data)
                    outfile.write(encrypted)


    def decrypt(self, in_filename, out_filename, key):

        with open(in_filename, "rb") as infile:
            filesize_bytes = infile.read(self.FILE_SIZE)
            filesize = int.from_bytes(filesize_bytes, self.BYTE_ORDER)
            iv = infile.read(self.IV_SIZE)
            
            with open(out_filename, "wb") as outfile:
                enc_key = SHA256.new(key.encode()).digest()
                # Create AES cipher object from the enc_key and iv
                cipher = AES.new(enc_key, self.mode, iv)

                while True:
                    data = infile.read(self.FILE_BLOCK_SIZE)
                    data_len = len(data)
                    if data_len == 0:
                        break

                    # Decrypte data, and write it to the outfile.
                    decrypted = cipher.decrypt(data)

                    outfile.write(decrypted)
                    # Truncate the outfile to be the original filesize
                    outfile.truncate(filesize)

