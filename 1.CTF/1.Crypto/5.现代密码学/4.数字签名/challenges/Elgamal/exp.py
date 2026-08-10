from pwn import *
from hashlib import sha256
from sympy.ntheory.modular import crt

hash = lambda msg: int(sha256(msg).hexdigest(), 16)

# context(log_level = 'debug')

io = process(["python", r"C:\Users\SeanL\Desktop\教培打工\challenges\Elgamal\task.py"])

io.recvuntil(b"p: ")
p = int(io.recvline().strip())
io.recvuntil(b"g: ")
g = int(io.recvline().strip())
io.recvuntil(b"y: ")
y = int(io.recvline().strip())

io.recvuntil(b"msg: ")
msg = io.recvline().strip()
io.recvuntil(b"r: ")
r = int(io.recvline().strip())
io.recvuntil(b"s: ")
s = int(io.recvline().strip())

msg_ = b"Hello, this is a fake message to sign"
h = hash(msg)
h_ = hash(msg_)
k = h_*pow(h,-1, p-1) % (p-1)
s_ = k*s
r_ = crt([p-1,p],[k*r,r])[0]
print(r_)

io.sendlineafter(b"msg: ", msg_.decode())
io.sendlineafter(b"r: ", str(r_).encode())
io.sendlineafter(b"s: ", str(s_).encode())
print(io.recvline().strip().decode())

io.close()

# flag{this_will_show_you_how_to_hack_elgamal}