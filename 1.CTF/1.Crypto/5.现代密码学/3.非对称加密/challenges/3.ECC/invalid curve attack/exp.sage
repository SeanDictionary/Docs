__import__('os').environ['TERM'] = 'xterm'
__import__('warnings').filterwarnings("ignore", category=RuntimeWarning)

from pwn import *
from Crypto.Util.number import *
import signal

io = process(["python", r"/home/sean/task.py"])

def DLP():
    while True:
        p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
        b = randint(0, p)
        E = EllipticCurve(GF(p), [a, b])
        order = E.order()
        try:
            signal.alarm(3)
            factors = prime_factors(order)
            signal.alarm(0)
        except:
            continue
        prime = 0
        for factor in factors:
            prime = factor
            if factor > 2**20:
                break
        if prime != 0:
            break

    G = E.gen(0) * (order // prime)
    Gx, Gy = G.xy()
    io.sendlineafter("Enter x coordinate:", str(Gx).encode())
    io.sendlineafter("Enter y coordinate:", str(Gy).encode())
    data = io.recvline().strip().decode().split(", ")
    Qx, Qy = int(data[0][1:]), int(data[1][:-1])
    Q = E(Qx, Qy)
    try:
        signal.alarm(3)
        log = G.discrete_log(Q)
        signal.alarm(0)
        return log, prime
    except:
        return DLP()

dlogs = []
primes = []
for i in range(10):
    log, prime = DLP()
    print(f"{i}: {log}, {prime}")
    dlogs.append(log)
    primes.append(prime)
m = crt(dlogs, primes)
print(long_to_bytes(int(m)))

io.interactive()

# flag{invalid_curve_attack}
