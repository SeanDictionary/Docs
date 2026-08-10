import itertools
from pathlib import Path

import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib


Q = 65537
NOISE_BOUND = 2

K1 = np.array([
    [1, 0, -1],
    [2, 0, -2],
    [1, 0, -1],
], dtype=np.int64)

K2 = np.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1],
], dtype=np.int64)

MIX = np.array([
    [5312, 11457, 22011, 991, 30123, 441, 12009, 17777],
    [20001, 9182, 7711, 5412, 1322, 9911, 4444, 25111],
    [31111, 721, 18008, 6191, 17001, 1200, 9222, 6611],
    [12345, 22222, 3333, 8765, 11111, 7001, 8080, 19001],
    [55555, 1111, 22221, 3333, 4444, 5555, 6666, 7777],
    [9012, 34001, 8123, 9101, 12001, 1300, 4441, 7771],
    [16001, 17001, 18001, 19001, 20001, 21001, 22001, 23001],
    [54321, 12321, 7777, 9999, 13579, 2468, 1111, 22229],
], dtype=np.int64) % Q


def conv_valid(x: np.ndarray, k: np.ndarray) -> np.ndarray:
    h, w = x.shape
    kh, kw = k.shape
    out = np.zeros((h - kh + 1, w - kw + 1), dtype=np.int64)
    for i in range(h - kh + 1):
        for j in range(w - kw + 1):
            out[i, j] = int(np.sum(x[i:i + kh, j:j + kw] * k))
    return out


def relu(x: np.ndarray) -> np.ndarray:
    return np.maximum(x, 0)


def avgpool2x2(x: np.ndarray) -> np.ndarray:
    out = np.zeros((2, 2), dtype=np.int64)
    for i in range(2):
        for j in range(2):
            block = x[2 * i:2 * i + 2, 2 * j:2 * j + 2]
            out[i, j] = int(np.sum(block) // 4)
    return out


def feature(x: np.ndarray) -> np.ndarray:
    c1 = avgpool2x2(relu(conv_valid(x, K1)))
    c2 = avgpool2x2(relu(conv_valid(x, K2)))
    base = np.concatenate([c1.reshape(-1), c2.reshape(-1)]).astype(np.int64)
    return (MIX @ base) % Q


def inv_mod_matrix(mat: np.ndarray, mod: int) -> np.ndarray:
    mat = mat.copy() % mod
    n = mat.shape[0]
    ident = np.eye(n, dtype=np.int64)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if int(mat[row, col]) % mod != 0:
                pivot = row
                break
        if pivot is None:
            raise ValueError("matrix is singular modulo q")
        if pivot != col:
            mat[[col, pivot]] = mat[[pivot, col]]
            ident[[col, pivot]] = ident[[pivot, col]]
        inv = pow(int(mat[col, col]), -1, mod)
        mat[col] = (mat[col] * inv) % mod
        ident[col] = (ident[col] * inv) % mod
        for row in range(n):
            if row == col:
                continue
            factor = int(mat[row, col])
            if factor:
                mat[row] = (mat[row] - factor * mat[col]) % mod
                ident[row] = (ident[row] - factor * ident[col]) % mod
    return ident % mod


def independent_rows_mod(mat: np.ndarray, mod: int) -> list[int]:
    work = mat.copy() % mod
    rows, cols = work.shape
    chosen = []
    pivot_row = 0
    for col in range(cols):
        pivot = None
        for row in range(pivot_row, rows):
            if int(work[row, col]) % mod != 0:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != pivot_row:
            work[[pivot_row, pivot]] = work[[pivot, pivot_row]]
        inv = pow(int(work[pivot_row, col]), -1, mod)
        work[pivot_row] = (work[pivot_row] * inv) % mod
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = int(work[row, col])
            if factor:
                work[row] = (work[row] - factor * work[pivot_row]) % mod
        chosen.append(pivot if pivot == pivot_row else pivot)
        pivot_row += 1
        if pivot_row == cols:
            break

    if len(chosen) != cols:
        raise ValueError("failed to find full-rank row set")

    # Re-run elimination on row indices to preserve original positions.
    chosen = []
    basis = []
    for idx, row in enumerate(mat % mod):
        trial = np.array(basis + [row], dtype=np.int64)
        if np.linalg.matrix_rank(trial.astype(np.float64)) > len(basis):
            chosen.append(idx)
            basis.append(row)
        if len(chosen) == cols:
            break
    if len(chosen) != cols:
        raise ValueError("failed to recover original full-rank rows")
    return chosen


def center_mod(vec: np.ndarray, mod: int) -> np.ndarray:
    centered = vec.copy()
    centered = np.where(centered > mod // 2, centered - mod, centered)
    return centered


def recover_secret(a_mat: np.ndarray, b_vec: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    idx = independent_rows_mod(a_mat, Q)
    a_sub = a_mat[idx] % Q
    b_sub = b_vec[idx] % Q
    a_sub_inv = inv_mod_matrix(a_sub, Q)
    s0 = (a_sub_inv @ b_sub) % Q
    errors = np.array(list(itertools.product(range(-NOISE_BOUND, NOISE_BOUND + 1), repeat=len(idx))), dtype=np.int64)
    candidates = (s0 - (errors @ a_sub_inv.T)) % Q

    for start in range(0, len(candidates), 5000):
        chunk = candidates[start:start + 5000]
        pred = (a_mat @ chunk.T) % Q
        resid = center_mod((b_vec.reshape(-1, 1) - pred) % Q, Q)
        ok = np.all(np.abs(resid) <= NOISE_BOUND, axis=0)
        if np.any(ok):
            secret = chunk[ok][0]
            full_resid = center_mod((b_vec - (a_mat @ secret) % Q) % Q, Q)
            return secret, full_resid

    raise ValueError("no valid secret found")


def decrypt_flag(secret_signed: list[int], cipher: bytes) -> str:
    key_material = ",".join(map(str, secret_signed)).encode()
    key = hashlib.sha256(key_material).digest()[:16]
    plain = AES.new(key, AES.MODE_ECB).decrypt(cipher)
    return unpad(plain, 16).decode()


def main() -> None:
    base = Path("task")
    inputs = np.load(base / "inputs.npy")
    outputs = np.load(base / "outputs.npy").astype(np.int64)
    cipher = (base / "cipher.bin").read_bytes()

    a_mat = np.array([feature(x) for x in inputs], dtype=np.int64)
    secret_mod, residuals = recover_secret(a_mat, outputs)
    secret_signed = center_mod(secret_mod, Q).astype(int).tolist()
    flag = decrypt_flag(secret_signed, cipher)

    print("secret_s (signed) =", secret_signed)
    print("residuals =", residuals.astype(int).tolist())
    print("flag =", flag)


if __name__ == "__main__":
    main()
