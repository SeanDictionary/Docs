from util import Elgamal

flag = b"flag{this_will_show_you_how_to_hack_elgamal}"

elgamal = Elgamal()

print("ElGamal parameters:")
print("p:", elgamal.p)
print("g:", elgamal.g)
print("y:", elgamal.y)

msg = b"Hello, this is a message to sign"
signature = elgamal.sign(msg)
print("Signature:")
print("msg:", msg.decode())
print("r:", signature[0])
print("s:", signature[1])

print("Input your signature to verify:")
msg_ = input("msg: ").encode()
r = int(input("r: "))
s = int(input("s: "))

if msg_ != msg:
    if elgamal.verity(msg_, (r, s)):
        print(flag.decode())
    else:
        print("Signature verification failed.")
else:
    print("Don't try to use the same message as the original one.")



