from Crypto.Util.number import *
from pwn import *

# context(log_level = 'debug')

io = process(["python", r"C:\Users\SeanL\Desktop\教培打工\challenges\RSA Byte Oracle\task.py"])

io.recvuntil(b"n: ")
n = int(io.recvline().strip())
io.recvuntil(b"Enter your choice:")
io.sendline(b"G")
io.recvuntil(b"Encrypt flag: ")
c = int(io.recvline().strip())

k = 0
tmp = pow(n, -1, 256)
for i in range(1, 1024//8+1):
    io.recvuntil(b"Enter your choice:")
    io.sendline(b"D")
    
    io.recvuntil(b"Your message:")
    a = pow(256**i, 65537, n)
    io.sendline(str(a*c).encode())
    io.recvuntil(b"Decrypt message(decimal): ")
    output = int(io.recvline().strip())
    t = -tmp*output % 256
    k = 256*k + t
    m = long_to_bytes((k+1)*n//256**(1024//8))
    print(m)

io.close()
