import openai
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64


# generating keys for third party
def gen():
    new_key = RSA.generate(4096, e = 65537)
    private_key = new_key.exportKey('PEM')
    public_key = new_key.publickey().exportKey('PEM')
    f = open('private_key(third_party).pem', 'wb')
    f.write(private_key)
    f.close()

    f = open('public_key(third_party).pem', 'wb')
    f.write(public_key)
    f.close()

#ecrpytion
def encrypt_blob(blob, public_key):
    rsa_key = RSA.importKey(public_key)  
    rsa_key = PKCS1_OAEP.new(rsa_key)  

    blob = zlib.compress(blob.encode('utf-8')) 

    chunk_size = 470 
    offset = 0  
    end_loop = False 
    encrypted = b''  

    while not end_loop:
        chunk = blob[offset:offset + chunk_size]  
        if len(chunk) < chunk_size:  
            end_loop = True  

        encrypted += rsa_key.encrypt(chunk)  

        offset += chunk_size 

    return base64.b64encode(encrypted).decode('utf-8')  

#decryption
def decrypt_blob(encrypted_blob, private_key):
    rsa_key = RSA.import_key(private_key)
    rsa_cipher = PKCS1_OAEP.new(rsa_key)

    encrypted_blob = base64.b64decode(encrypted_blob)

    chunk_size = rsa_key.size_in_bytes()
    offset = 0
    decrypted = b''

    while offset < len(encrypted_blob):
        chunk = encrypted_blob[offset:offset + chunk_size]
        decrypted += rsa_cipher.decrypt(chunk)
        offset += chunk_size

    try:
        return zlib.decompress(decrypted).decode('utf-8')  
    except zlib.error:
        return decrypted.decode('utf-8') 