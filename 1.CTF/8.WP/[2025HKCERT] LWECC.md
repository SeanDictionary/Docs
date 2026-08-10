# 题目

```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
from random import choice
from hashlib import md5
from secret import flag
  
p = 1096126227998177188652856107362412783873814431647
E = EllipticCurve(GF(p), [0, 5])
  
s = [E.random_element() for _ in range(73)]
e = [E.random_element() for _ in "01"]
A = random_matrix(GF(p), 137, 73)
b = [(sum(i*j for i,j in zip(_,s)) + choice(e)).xy() for _ in A]
  
 
print("A =", A.list())
print("b =", b)
print("enc =", AES.new(key=md5(str(s).encode()).digest(), nonce=b"LWECC", mode=AES.MODE_CTR).encrypt(flag))
```

# Exp

题目给出的是这样一个式子

$$
A_{137\times 73}\cdot s_{73\times 1}+e_{137\times 1}=b_{137\times 1}
$$

然后误差向量 $e\in\{e_0,e_1\}^{137}$，所以可以进行一个变换，令标量 $\Delta = e_1-e_0$，向量 $\delta\in\{0,1\}^{137}$

$$
[A|I_{137\times 1}]_{137\times 74}\cdot \left[\frac{s}{e_0}\right]_{74\times 1}+\delta_{137\times 1}\Delta=b_{137\times 1}
$$

令 $M=[A|I]_{137\times 74}$，并计算 $M$ 的左核空间 $V$，核空间的维度为 $137-74=63$，取 $V$ 的一组基 $\{v_1,v_2,\cdots,v_{63}\}$，带入上式，得到

$$
\begin{align*}
 &V_{63\times 137}M\cdot \left[\frac{s}{e_0}\right]+V_{63\times 137}\delta\Delta\\
=&V\delta\Delta\\
=&Vb\\
\end{align*}
$$

注意到对于该给定的曲线 $E(\mathbb{F}_p)$，有 $order(E(\mathbb{F}_p))=p$，所以可以通过 _Smart Attack_ 将题给的点运算转换为标量运算，如下

$$
\left\{\begin{align*}
b&=(r_1G,r_2G,\cdots,r_{137}G)\\
&=(r_1,r_2,\cdots,r_{137})G\\
\\
\Delta&=r_\Delta G
\end{align*}\right.\Rightarrow
V\delta r_\Delta G=Vr_bG
$$

由于 $\Delta$ 未知，于是 $r_\Delta$ 也未知，所以我们可以利用第一行作为已知量，来消去 $r_\Delta$

$$
\begin{align*}
            &v_0\delta r_\Delta G=v_0r_bG\\
\Rightarrow &v_0\delta r_\Delta=v_0r_b\ mod\ p\\
\Rightarrow &r_\Delta=\frac{v_0r_b}{v_0\delta}\ mod\ p\\
\end{align*}
$$

对于其余 63 个向量，可以得到

$$
\begin{align*}
            &v_m\delta r_\Delta=v_mr_b\ mod\ p\\
\Rightarrow &v_m\delta=\frac{v_mr_b}{v_0r_b}v_0\delta\ mod\ p\\
\Rightarrow &\left(v_m-\frac{v_mr_b}{v_0r_b}v_0\right)\delta=0\ mod\ p\\
\end{align*}
$$

令 $u_m=\left(v_m-\frac{v_mr_b}{v_0r_b}v_0\right)$ 然后类似背包问题，可以构造格

$$
U=(u_1,u_2,\cdots,u_{62})_{137\times 62}
$$

$$
(\delta_0,\cdots,\delta_{136},k_1,\cdots,k_{62})
\left(\begin{array}{c|c}
I_{137\times 137}&U_{137\times 62}\\
\hline
0_{62\times 137}&p\cdot I_{62\times 62}\\
\end{array}\right)
=(\delta_0,\cdots,\delta_{136},0,\cdots,0)
$$

然后需要进行配平，再对格规约，得到 $\delta$ 向量。于是能计算出 $r_\Delta=\frac{v_0r_b}{v_0\delta}\ mod\ p$

接着我们可以根据计算出来的 $\delta$ 来对每一个方程相应的去除 $\Delta$ 的影响。然后可以得到这样的式子

$$
As+e_0=b'
$$

将第一行作为基准行，其他行减去第一行，得到

$$
A'_{136\times 73}s=b'_{136\times 1}
$$

解线性方程组得到 $s$，最后使用 AES 解密得到 flag。

```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import md5

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

enc = b"\xff\x167-S\x94\xf9$36\xa2\xb2\x89\x18a\xfd\xbb^\x0b1\xa6\xcc\x89\xb1Y\x0c\x9brO\x0bY\xbaR:'\xc7"
A = [...]
b = [(...)...]
p = 1096126227998177188652856107362412783873814431647
K = 2*120
E = EllipticCurve(GF(p), [0, 5])

G = E.gens()[0]

A = Matrix(GF(p), 137, 73, A)
b = [E(point) for point in b]
bb = [SmartAttack(G, point, p) for point in b]
rb = vector(GF(p), bb)
M = block_matrix([[A, ones_matrix(GF(p), 137, 1)]])
kernel = M.left_kernel()
basis = kernel.basis()
v0 = basis[0]
U = column_matrix(ZZ, [basis[i] - (basis[i]*rb)/(v0*rb)*v0 for i in range(1, 63)])

Ge = block_matrix(ZZ, [[identity_matrix(ZZ, 137), K*U], [Matrix(ZZ, 62, 137), K*p*identity_matrix(ZZ, 62)]])
L = Ge.LLL()

for row in L:
    if list(row)[137:] == [0]*62:
        if set(row) <= {0,1}:
            delta = list(row)[:137]
            print("Find δ:", delta)
            break

V_delta = vector(GF(p), delta)
r_delta = (v0*rb)/(v0*V_delta)

rb -= vector(GF(p), [r_delta if delta[i] == 1 else 0 for i in range(137)])
rb_ = rb[1:] - vector([rb[0]] * (len(rb)-1))
A_ = A[1:] - Matrix([A[0]] * (A.nrows()-1))
rs = A_.solve_right(rb_)
s = [tmp*G for tmp in rs]
cipher = AES.new(key=md5(str(s).encode()).digest(), nonce=b"LWECC", mode=AES.MODE_CTR)
flag = cipher.decrypt(enc)
print(flag)
```