import json
import random
import numpy as np
import os


q = 65537  
NOISE_BOUND = 2  
NUM_SAMPLES = 24  


K1 = np.array([
    [ 1,  0, -1],
    [ 2,  0, -2],
    [ 1,  0, -1]
], dtype=np.int64)

K2 = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1]
], dtype=np.int64)


MIX = np.array([
    [  5312, 11457, 22011,  991, 30123, 441, 12009, 17777],
    [ 20001,  9182,  7711, 5412,  1322, 9911, 4444, 25111],
    [ 31111,   721, 18008, 6191, 17001, 1200, 9222,  6611],
    [ 12345, 22222,  3333, 8765, 11111, 7001, 8080, 19001],
    [ 55555,  1111, 22221, 3333,  4444, 5555, 6666,  7777],
    [  9012, 34001,  8123, 9101, 12001, 1300, 4441,  7771],
    [ 16001, 17001, 18001, 19001, 20001, 21001, 22001, 23001],
    [ 54321, 12321,  7777, 9999, 13579, 2468, 1111, 22229],
], dtype=np.int64) % q


secret_s = 


def conv_valid(x, k):
    h, w = x.shape
    kh, kw = k.shape
    out = np.zeros((h-kh+1, w-kw+1), dtype=np.int64)
    for i in range(h-kh+1):
        for j in range(w-kw+1):
            out[i, j] = int(np.sum(x[i:i+kh, j:j+kw] * k))
    return out

def relu(x):
    return np.maximum(x, 0)

def avgpool2x2(x):
    out = np.zeros((2, 2), dtype=np.int64)
    for i in range(2):
        for j in range(2):
            block = x[2*i:2*i+2, 2*j:2*j+2]
            out[i, j] = int(np.sum(block) // 4)
    return out

def feature(x):
    c1 = avgpool2x2(relu(conv_valid(x, K1)))  
    c2 = avgpool2x2(relu(conv_valid(x, K2)))  
    base = np.concatenate([c1.reshape(-1), c2.reshape(-1)]).astype(np.int64)  
    mixed = (MIX @ base) % q
    return mixed.astype(np.int64)


def add_noise_to_output(a, secret_s, noise_bound, q):

    e = random.randint(-noise_bound, noise_bound)
    b_i = int(np.dot(a, secret_s) + e) % q
    return b_i

def generate_outputs(inputs, secret_s, noise_bound, q):
    outputs = []
    for x in inputs:
        a = feature(x)  
        b = add_noise_to_output(a, secret_s, noise_bound, q)  
        outputs.append(b)
    return np.array(outputs, dtype=np.int64)


for i in range(1, 11):

    inputs = np.random.randint(0, 8, size=(NUM_SAMPLES, 6, 6), dtype=np.int64)
    outputs = generate_outputs(inputs, secret_s, NOISE_BOUND, q)

    folder_name = f"附件{i}"
    os.makedirs(folder_name, exist_ok=True)

    np.save(os.path.join(folder_name, "inputs.npy"), inputs)
    np.save(os.path.join(folder_name, "outputs.npy"), outputs)

    with open(os.path.join(folder_name, "public.json"), "w") as f:
        json.dump({
            "q": q,
            "noise_bound": NOISE_BOUND,
            "kernels": {
                "K1": K1.tolist(),
                "K2": K2.tolist()
            },
            "mix": MIX.tolist(),
            "desc": "Recover the hidden integer head of a tiny CNN-like model."
        }, f, indent=2)

    print(f"[+] Created {folder_name}")