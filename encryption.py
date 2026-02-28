import os
from cryptography.fernet import Fernet

# Load or generate encryption key
KEY_FILE = "encryption.key"

def get_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key

key = get_or_create_key()
cipher = Fernet(key)

def encrypt_message(message):
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(token):
    return cipher.decrypt(token.encode()).decode()
