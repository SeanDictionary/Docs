from Crypto.Util.number import getPrime, isPrime, inverse
from hashlib import sha256
from random import randint

class Elgamal:
	def __init__(self):
		self.p, self.g = self._gen()
		self.d = randint(0, self.p - 2)
		self.y = pow(self.g, self.d, self.p)

	def _gen(self): 
		q = 8867984692712162589394753592684462893849721383808359270870591946309591420901509987341888487540800853389811701998166292427185543648905432008953442556844003
		p = 2*q + 1
		while True:
			if isPrime(p):
				g = randint(2,p-1)
				if (pow(g,2,p) != 1) & (pow(g,q,p) != 1):
					break
		return p,g

	def _hash(self, msg): 
		#哈希函数
		return int(sha256(msg).hexdigest(),16)

	def sign(self, msg): 
		#签名函数
		m = self._hash(msg)
		phi = self.p - 1

		while True:
			k = getPrime(512)
			if k < phi : break

		r = pow(self.g, k, self.p)
		s = ((m - self.d * r) * inverse(k,phi)) % (phi)
		return (r,s)

	def verity(self, msg, Signature):
		#验签函数
		m = self._hash(msg)
		r,s = Signature

		A = (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p
		B = pow(self.g, m, self.p)

		if A == B:
			return True
		else:
			return False