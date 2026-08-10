# 现代密码学

## 流密码

### LCG

#### 未知参量

#### 随机 b

#### 已知 seed 高位

#### 已知 seed 低位

#### Gröbner 基 [文章](https://thr-sec.com/posts/gr%C3%B6bner-%E5%9F%BA%E5%AD%A6%E4%B9%A0/)

---

### LFSR [文章](https://tangcuxiaojikuai.xyz/post/c2c51200.html)

#### correlation attack

#### fast correlation attack

#### 归零子式

---

### RC4

#### FMS Attack

##### [Crypto Hack] Oh SNAP

---

### MT19937

---

### Salsa20

#### ChaCha20

---

### Rabbit

---

## 块加密

### AES

#### EBC

#### CBC

##### 字节反转攻击

##### Padding Oracle

##### 选择明文/密文攻击

#### OFB

#### CTR

#### CFB

##### CFB8

##### CFB1

#### 积分攻击

#### 差分攻击

---

### DES

#### DES 弱密钥

#### DDES

#### TDES

---

## 非对称加密

### RSA

#### 泄露

##### dp,dq 泄露

##### dp 泄露

##### Coppersmith

###### 已知 p 高位

###### 已知 m 高位

###### 已知 d 高位

###### 多元 Coppersmith

##### 剪枝

##### 已知 phi 分解

#### 共模攻击

#### 广播攻击

#### 维纳攻击

##### 扩展维纳攻击

#### Boneh Durfee 攻击

#### e 和 phi 不互质 / AMM

#### Rabin 加密

#### MatrixRSA

#### ROCA

#### hash length extension attack

#### Padding oracle attack

---

### DSA

---

### ECC

#### ECDLP

#### Smart’s Attack

#### MOV attack

#### 双线性配对

#### invalid curve attack

---

### 背包密码

---

### ElGamal

---

### Diffie-Hellman 密钥交换算法

---

### 格密码

#### SVP

#### CVP

##### Babai Algorithm

#### NTRU [文章](https://tover.xyz/p/NTRU)

#### GGH 加密

#### HNP

##### LHNP

##### MIHNP

##### ECHNP

#### LLBP

#### HSP

#### HSSP

##### AHSSP

#### HLCP

#### LWE

#### AGCD

---

## 哈希函数

### SHA1

---

### SHA256

---

### MD5

---

### FNV

#### 碰撞

---

## 数字签名

### RSA

#### PEM

#### CRT

#### SSH

---

### DSA

#### ECDSA

---

### ElGamal

#### 伪造签名(验签漏洞)

---

# 数学

## 离散对数/DLP

### 整数 DLP

#### BSGS

#### Pollard rho

#### Pohlig Hellman

### 矩阵 DLP

### ECDLP

---

## 抽象代数

### 群论

#### 多项式环

##### 商环

---

## 线性代数

---

## 其他

### 四元数

---

# CVE

## `CVE-2012-4929 Crime漏洞`

### [CryptoHack] CTRIME

## `CVE-2017-15361 ROCA漏洞`

### [2025HGAME] suprimeRSA

## `CVE-2020-1472  ZeroLogon漏洞`

### [CryptoHack] Logon Zero

---

# 出题思路

## ✅ 四元数

## ❎ 通过加密算法的时间复杂度来实现基于时间的侧信道攻击

## ❎ AGM算术几何平均数

## ✅ flag用非ASCII字符
