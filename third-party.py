from crypto import encrypt_blob, gen
from load import upload_file_to_mega, download_file_from_mega
from mega import Mega
import shutil
import os

# 生成密鑰對
gen()

# 讀取公鑰
with open('public_key(third_party).pem', 'rb') as f:
    public_key = f.read()

# 初始化 Mega 並登錄
mega = Mega()
email = "eric23101983@gmail.com"  # 替換為你的 Mega 帳號
password = "124215545451542212"   # 替換為你的 Mega 密碼
m = mega.login(email, password)
    

# 加密並上傳檔案的函數
def process_and_upload(x, file_name, enc_file_name):
    try:
        content = download_file_from_mega(m, f'H_{x}', file_name)
        path = os.path.join(f'H_{x}', file_name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

        # 加密檔案內容
        encrypted_text = encrypt_blob(content, public_key)
        
        upload_file_to_mega(m, f'K_{x}',enc_file_name, encrypted_text)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")

count = 1
while True:
    try:
        # 生成檔案名
        hash_a = f'H(A{count}).txt'
        hash_b = f'H(B{count}).txt'
        enc_h_a = f'K(A{count}).txt'
        enc_h_b = f'K(B{count}).txt'

        # 處理並上傳檔案
        process_and_upload('A', hash_a, enc_h_a)
        file_handle = m.find('stop/stop.txt')
        if file_handle:
            print("Ending process")
            break
        print(f'A{count} --> B{count} accomplished')
        process_and_upload('B', hash_b, enc_h_b)
        print(f'B{count} --> A{count+1} accomplished')

        count += 1
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        break  # 停止無限迴圈

