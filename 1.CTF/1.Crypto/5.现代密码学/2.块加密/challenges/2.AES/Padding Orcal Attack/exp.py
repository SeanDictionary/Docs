from pwn import *
import os


def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


def padding_oracle(block1, block2):
    decrypted = [0] * 16
    for i in range(1, 17):
        target = os.urandom(16 - i) + bytes([i]) * i
        for j in range(256):
            decrypted[-i] = j
            payload = xor(xor(block1, decrypted), target) + block2
            io.sendlineafter(b':', payload.hex().encode())
            result = io.recvline().strip().decode()
            if result == "success":
                print(f"{i:>2} | {' '.join(f'{x:>3}' for x in decrypted)}")
                break
        else:
            raise Exception(f"{i} padding oracle failed")

    return decrypted


def attack(blocks):
    plaintext = b""
    for i in range(1, len(blocks)):
        print(f"[+] block {i}")
        decrypted = padding_oracle(blocks[i - 1], blocks[i])
        plaintext += bytes(decrypted)
    return plaintext


io = process(["python", r"C:\Users\SeanL\Desktop\CTF_CRYPTO\密码学授课\密码总览\challenges\Padding Orcal Attack\task.py"])

io.recvuntil(b'Ciphertext:')
ciphertext = bytes.fromhex(io.recvline().strip().decode())
blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]

plaintext = attack(blocks)
print(plaintext)
