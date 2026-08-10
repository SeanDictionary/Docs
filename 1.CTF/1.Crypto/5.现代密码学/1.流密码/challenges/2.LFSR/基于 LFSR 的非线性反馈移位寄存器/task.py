from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import md5
from secret import flag, seed, mask


class LFSR2:
    def __init__(self, n, seed, mask, lfsr=None):
        self.state = [int(b) for b in f"{seed:0{n}b}"]
        self.mask_bits = [int(b) for b in f"{mask:0{n}b}"]
        self.n = n
        self.lfsr = lfsr

    def update(self):
        s = sum([self.state[i] * self.mask_bits[i] for i in range(self.n)]) & 1
        self.state = self.state[1:] + [s]

    def __call__(self):
        if self.lfsr:
            if self.lfsr():
                self.update()
            return self.state[-1]
        else:
            self.update()
            return self.state[-1]


class LFSR1(LFSR2):
    def __init__(self, n, seed, mask):
        super().__init__(n, seed, mask, lfsr=None)


n = 64
assert seed.bit_length() == mask.bit_length() == n
lfsr1 = LFSR1(n, seed, mask)
lfsr2 = LFSR2(n, seed, mask, lfsr1)
print(f"mask = {mask}")
print(f"output = {sum(lfsr2() << (n - 1 - i) for i in range(n))}")
print(f"enc = {AES.new(key=md5(str(seed).encode()).digest(), mode=AES.MODE_ECB).encrypt(pad(flag, 16))}")
# mask = 9494051593829874780
# output = 13799267741689921474
# enc = b'\x03\xd1#\xb9\xaa5\xff3y\xba\xcb\x91`\x9d4p~9r\xf6i\r\xca\x03dW\xdb\x9a\xd2\xa6\xc6\x85\xfa\x19=b\xb2)5>]\x05,\xeb\xa0\x12\xa9\x1e'