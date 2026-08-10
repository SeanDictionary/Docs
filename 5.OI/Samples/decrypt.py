import base64
from Crypto.Cipher import AES, Blowfish
from gmssl.sm4 import CryptSM4, SM4_DECRYPT

def pad_key(key, length):
    """
    将密钥填充到指定长度
    """
    return key.encode('utf-8')[:length].ljust(length, b'\0')

def decrypt_aes(key, encrypted_content):
    """
    使用 AES ECB模式解密
    """
    try:
        key_bytes = pad_key(key, 16)
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted_bytes = base64.b64decode(encrypted_content)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.rstrip(b'\x00').decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"AES 解密失败: {e}")

def decrypt_blowfish(key, encrypted_content):
    """
    使用 Blowfish ECB模式解密
    """
    try:
        key_bytes = pad_key(key, 16)
        cipher = Blowfish.new(key_bytes, Blowfish.MODE_ECB)
        encrypted_bytes = base64.b64decode(encrypted_content)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return decrypted_bytes.rstrip(b'\x00').decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Blowfish 解密失败: {e}")

def decrypt_sm4(key, encrypted_content):
    """
    使用 SM4 解密
    """
    try:
        key_bytes = pad_key(key, 16)
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(key_bytes, SM4_DECRYPT)
        encrypted_bytes = base64.b64decode(encrypted_content)
        decrypted_bytes = crypt_sm4.crypt_ecb(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"SM4 解密失败: {e}")

# 示例调用
if __name__ == "__main__":
    key = ""
    encrypted_aes = ""
    encrypted_blowfish = ""
    encrypted_sm4 = ""

    try:
        decrypted_aes = decrypt_aes(key, encrypted_aes)
        print(f"AES 解密结果: {decrypted_aes}")
    except Exception as e:
        print(e)

    try:
        decrypted_blowfish = decrypt_blowfish(key, encrypted_blowfish)
        print(f"Blowfish 解密结果: {decrypted_blowfish}")
    except Exception as e:
        print(e)

    try:
        decrypted_sm4 = decrypt_sm4(key, encrypted_sm4)
        print(f"SM4 解密结果: {decrypted_sm4}")
    except Exception as e:
        print(e)