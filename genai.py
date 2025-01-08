import openai
import os
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64
from crypto import gen, decrypt_blob, encrypt_blob
from load import login_to_mega, upload_file_to_mega, download_file_from_mega

import threading
from mega import Mega
import socket
import hashlib

openai.api_key = "EMPTY"
openai.api_base = "http://140.112.18.217:8080"
model = "Llama3"

# login to mega & connect
mega = Mega()
m = mega.login('eric23101983@gmail.com', '124215545451542212')


# generate keys & input keys

with open('public_key.pem', 'rb') as f:
    public_key = f.read()
with open('private_key.pem', 'rb') as f:
    private_key = f.read()

local_path = '/Desktop/web_project'
# start running
count = 1


ea_file = 'E(A{}).txt'.format(count)
ask_org = download_file_from_mega(m, 'E_A', ea_file)
ask = decrypt_blob(ask_org, private_key)
print('A ask: ' + ask +'\n')

if ask == 'stop':
	quit()

message = [{"role": "user", "content": ask}]
completion = openai.ChatCompletion.create(
	model=model,
	messages=message,
	max_tokens=1800
)
reply = completion.choices[0].message.content


ka_file = 'K(A{}).txt'.format(count)
sig = download_file_from_mega(m, 'K_A', ka_file)

block = reply + sig + ask
record = reply + '\n' + sig + '\n' + ask

path = os.path.join('B_log', 'B{}.txt'.format(count))
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'a') as f:
	f.write(record)

ans = encrypt_blob(reply, public_key)
upload_file_to_mega(m, 'E_B','E(B{}).txt'.format(count), ans)

hash = hashlib.md5(block.encode('utf-8')).hexdigest()
upload_file_to_mega(m, 'H_B', 'H(B{}).txt'.format(count), hash)

print(reply+"\n")

message.append({"role": "assistant", "content": reply})

while True:
	count += 1

	ea_file = 'E(A{}).txt'.format(count)
	ask_org = download_file_from_mega(m, 'E_A', ea_file)
	ask = decrypt_blob(ask_org, private_key)

	print('A ask: ' + ask +'\n')

	if ask == "stop":
		break

	message.append({"role": "user", "content": ask})
	completion = openai.ChatCompletion.create(
		model=model,
		messages=message,
		max_tokens=1800
	)
	reply = completion.choices[0].message.content

	ka_file = 'K(A{}).txt'.format(count)
	sig = download_file_from_mega(m, 'K_A', ka_file)

	block = reply + sig + ask_org
	record = reply + '\n' + sig + '\n' + ask

	with open(os.path.join('B_log', 'B{}.txt'.format(count)),'a') as f:
		f.write(record)

	ans = encrypt_blob(reply, public_key)
	upload_file_to_mega(m, 'E_B', 'E(B{}).txt'.format(count), ans)

	hash = hashlib.md5(block.encode('utf-8')).hexdigest()
	upload_file_to_mega(m, 'H_B','H(B{}).txt'.format(count), hash)

	print(reply+"\n")

	message.append({"role": "assistant", "content": reply})