from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def decrypt(data):
    data = bytes.fromhex(data)
    IV, C = data[:16],  data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    result = cipher.decrypt(C)
    return result


flag = b"flag{y0u_1e4rned_P4dd1ng_0rac13_Att4ck}"

plaintext = pad(flag, 16)
KEY = os.urandom(16)
IV = os.urandom(16)
cipher = AES.new(KEY, AES.MODE_CBC, IV)
ciphertext = IV + cipher.encrypt(plaintext)

print("Ciphertext:", ciphertext.hex())

while True:
    ciphertext = input("(0 to exit)Your ciphertext:")
    if ciphertext == "0":
        break
    try:
        plaintext = unpad(decrypt(ciphertext), 16)
        print("success")
    except:
        print("error")