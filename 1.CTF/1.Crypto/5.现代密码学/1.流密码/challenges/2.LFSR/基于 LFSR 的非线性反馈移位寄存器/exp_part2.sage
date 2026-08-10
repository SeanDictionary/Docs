from Crypto.Cipher import AES
from hashlib import md5
from Crypto.Util.Padding import unpad
 
enc = b'\x03\xd1#\xb9\xaa5\xff3y\xba\xcb\x91`\x9d4p~9r\xf6i\r\xca\x03dW\xdb\x9a\xd2\xa6\xc6\x85\xfa\x19=b\xb2)5>]\x05,\xeb\xa0\x12\xa9\x1e'
 
mask = [int(b) for b in f"{9494051593829874780:0{64}b}"]
 
def calc(state,n=64):
    A = Matrix(GF(2),[[0]*i + mask[:n-i] for i in range(n)])
    b = vector(GF(2),[state[i]-sum(state[j]*mask[n+j-i] for j in range(i)) for i in range(n)])
    try:
        return A.solve_right(b)
    except:
        return None
 
with open("output.txt","r") as f:
    tmp = f.read().split("\n")[:-1]
for k in tmp:
    state = [int(i) for i in k]
    res = calc(state)
    if res:
        seed = int("".join(str(i) for i in res),2)
        try:
            print(unpad(AES.new(key=md5(str(seed).encode()).digest(), mode=AES.MODE_ECB).decrypt(enc),16).decode())
        except:
            None
# flag{5b322a2b-8d15-43b3-88f0-ee1586f1cf4f}