

from cryptography.fernet import Fernet
from json import loads, dumps

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
    # encrypt data
    encrypted_data = f.encrypt(file_data)
    # write the encrypted file
    with open(f"{filename}.enc", "wb") as file:
        file.write(encrypted_data)

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(f"{filename}.dec", "wb") as file:
        file.write(decrypted_data)

def decrypt_json(filename, key) -> dict:
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrpted_data = file.read()
    decrypted_data = f.decrypt(encrpted_data)
    return loads(decrypted_data)

def encrypt_json(filename, key, content):
    f = Fernet(key)
    jsonstring = dumps(content)
    encryped_data = f.encrypt(bytes(jsonstring, encoding="utf-8"))
    with open(filename, "wb") as file:
        file.write(encryped_data)
    

