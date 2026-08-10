from Crypto.Util.number import *

MENU = """
Welcome to the RSA Byte Oracle!
-----------------------------
[G] Get encrypt flag
[D] Decrypt message
"""

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
d = pow(e, -1, (p-1)*(q-1))

flag = b"flag{OHHHHHHHHH_you_learned_RSA_byte_oracle_That's_so_cool!}"
m = bytes_to_long(flag)
c = pow(m, e, n)

print(MENU)
print(f"n: {n}")
while True:
    if input("Enter your choice:").strip().upper() == "G":
        print(f"Encrypt flag: {c}")
    else:
        msg = int(input("Your message:").strip())
        m = pow(msg, d, n)
        print(f"Decrypt message(decimal): {m%256}")


