import os
import socket
import threading
from mega import Mega


def login_to_mega():
    mega = Mega()
    m = mega.login('eric23101983@gmail.com', '124215545451542212')
    return m

def upload_file_to_mega(m, folder_name, file_name, content):
    file_path = file_name
    with open(file_path, 'a') as f:
        f.write(content)

    folder = m.find(folder_name)
    if not folder:
        folder = m.create_folder(folder_name)

    m.upload(file_path, folder[0])
    os.remove(file_path)

def download_file_from_mega(m, folder_name, file_name):
	file_handle = False
	while True:
		file_handle = m.find(os.path.join(folder_name, file_name))
		if file_handle:
			break
	m.download(file_handle)
	with open(file_name, 'r') as kb:
		sig = kb.read()
	os.remove(file_name)
	return sig
