from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtCore import QSize
import sys
import os
import hashlib
from Crypto.PublicKey import RSA
from crypto import encrypt_blob, decrypt_blob
from load import upload_file_to_mega, download_file_from_mega
from mega import Mega

# login to mega & connect
mega = Mega()
m = mega.login('eric23101983@gmail.com', '124215545451542212')

# input keys
with open('public_key.pem', 'rb') as f:
    public_key = f.read()
with open('private_key.pem', 'rb') as f:
    private_key = f.read()

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap("background.jpeg")  

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setOpacity(0.2)
        painter.drawPixmap(self.rect(), self.background_image) 
        super().paintEvent(event) 


class SingleWindowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure AI Interaction")
        self.resize(600, 400)

        # Load RSA Keys
        with open('public_key.pem', 'rb') as f:
            self.public_key = f.read()
        with open('private_key.pem', 'rb') as f:
            self.private_key = f.read()

        self.count = 0  # Transaction count

        # UI Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #D6EAF8;")
        main_layout = QVBoxLayout(central_widget)

        self.history_display = CustomTextEdit()
        self.history_display.setReadOnly(True)
        main_layout.addWidget(self.history_display)

        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Send message to AI")
        input_layout.addWidget(self.input_field)

        self.submit_button = QPushButton()
        self.submit_button.setIcon(QIcon("send.png"))
        self.submit_button.setIconSize(QSize(30, 30))
        self.submit_button.setFixedSize(40, 30)
        self.submit_button.clicked.connect(self.process_input)
        input_layout.addWidget(self.submit_button)
        
        self.sig = ''
        self.reply = ''

    def process_input(self):
        user_input = self.input_field.text()
        if user_input.strip():
            self.input_field.clear()

            sig = self.sig
            reply = self.reply
            block = user_input + sig + reply
            record = user_input + '\n' + sig + '\n' + reply

            self.count += 1

            # Encrypt and upload user input
            encrypted_input = encrypt_blob(user_input, self.public_key)
            upload_file_to_mega(m, "E_A", f"E(A{self.count}).txt", encrypted_input)

            # Generate hash of input and upload
            input_hash = hashlib.md5(block.encode('utf-8')).hexdigest()
            upload_file_to_mega(m, "H_A", f"H(A{self.count}).txt", input_hash)

            # Log user input locally
            path = os.path.join("A_log", f"A{self.count}.txt")
            if self.count == 1:
                os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a") as f:
                f.write(record)

            # Display user input in history
            user_html = f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="user.png" alt="User" width="30" height="30" style="margin-right: 10px;">
                    <span style="font-family: Arial; font-size: 20px; color: #000000;">{user_input}</span>
                </div>
            """
            self.history_display.append(user_html)

            if user_input == "stop":
                upload_file_to_mega(m, 'stop', 'stop.txt', ' ')
                quit()

			# Decrypt message from AI
            reply_org = download_file_from_mega(m, 'E_B', f'E(B{self.count}).txt')
            reply = decrypt_blob(reply_org, private_key)
            self.reply = reply

			# Get signature from the 3rd party
            sig = download_file_from_mega(m, 'K_B', f'K(B{self.count}).txt')
            self.sig = sig

			# Display AI output in history
            response_html = f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="robot.png" alt="AI" width="30" height="30" style="margin-right: 10px;">
                    <span style="font-family: Arial; font-size: 20px; color: #000000;">{reply}</span>
                </div>
            """
            self.history_display.append(response_html)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SingleWindowApp()
    window.show()
    sys.exit(app.exec_())