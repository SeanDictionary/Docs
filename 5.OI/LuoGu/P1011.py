def fei(n):
    if n in mem:
        return mem[n]
    mem[n] = fei(n-1) + fei(n-2)
    return mem[n]

def cal(n):
    an, bn = 0, 0
    for i in range(1,n):
        if i == 1 or i == 3:
            an += 1
            continue
        if i == 2:
            continue
        if i == 4:
            bn += fei(1)
            continue
        an += fei(i-4)
        bn += fei(i-3)
    return an,bn

mem = {1:1, 2:1}
a, n, m, x = map(int, input().split())
an, bn = cal(n)
ax, bx = cal(x+1)
try:
    b = (m-an*a)//bn
except:
    b = 0
print(ax*a + bx*b)