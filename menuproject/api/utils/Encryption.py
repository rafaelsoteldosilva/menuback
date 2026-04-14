import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv
import inspect

load_dotenv()

PASSWORDS_ENCRYPTION_KEY = os.getenv("PASSWORDS_ENCRYPTION_KEY")

def encrypt_value(value: str) -> str:
    cipher_suite = Fernet(PASSWORDS_ENCRYPTION_KEY) # type: ignore
    try:
        encrypted_value = cipher_suite.encrypt(value.encode())
        return encrypted_value.decode('utf-8')
    except Exception as e:
        print(f'Error in encrypt_value: {e}')  # Debug: Print any error that occurs
        raise

def decrypt_value(encrypted_value: str) -> str:
    # Check for None or empty string before attempting decryption
    if not encrypted_value:
        print("decrypt_value: Skipping decryption because value is None or empty")
        return ""
    
    cipher_suite = Fernet(PASSWORDS_ENCRYPTION_KEY)  # type: ignore
    try:
        decrypted_value = cipher_suite.decrypt(encrypted_value.encode())
        return decrypted_value.decode('utf-8')
    except Exception as e:
        print(f'Error in decrypt_value: {e}')  # Debug: Print any error that occurs
        raise
    
