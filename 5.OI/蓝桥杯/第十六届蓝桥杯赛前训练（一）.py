# 第十六届蓝桥杯赛前训练（一）
# 24/12/7
# A
# AC
""" lis = list(map(str,[5,6,8,6,9,1,6,1,2,4,9,1,9,8,2,3,6,4,7,7,5,9,5,0,3,8,7,5,8,1,5,8,6,1,8,3,0,3,7,9,2,
       7,0,5,8,8,5,7,0,9,9,1,9,4,4,6,8,6,3,3,8,5,1,6,3,4,6,7,0,7,8,2,7,6,8,9,5,6,5,6,1,4,0,1,
       0,0,9,4,8,0,9,1,2,8,5,0,2,5,3,3]))
day = [0,31,28,31,30,31,30,31,31,30,31,30,31]
ans = set()
n = len(lis)
box = [0]*8
for a in range(n-7):
    box[0] = lis[a]
    if lis[a] == "2":
        for b in range(a+1,n-6):
            box[1] = lis[b]
            if lis[b] == "0":
                for c in range(b+1,n-5):
                    box[2] = lis[c]
                    if lis[c] == "2":
                        for d in range(c+1,n-4):
                            box[3] = lis[d]
                            if lis[d] == "3":
                                for e in range(d+1,n-3):
                                    box[4] = lis[e]
                                    if lis[e] == "1" or lis[e] == "0":
                                        for f in range(e+1,n-2):
                                            box[5] = lis[f]
                                            if lis[e] == "0" and lis[f] != "0" or lis[e] == "1" and 0 <= int(lis[f]) <=2:
                                                for g in range(f+1,n-1):
                                                    box[6] = lis[g]
                                                    if 0 <= int(lis[g]) <=3:
                                                        for h in range(g+1,n):
                                                            box[7] = lis[h]
                                                            if day[int(lis[e] + lis[f])] >= int(lis[g] + lis[h]) > 0:
                                                                ans.add("".join(box[4:]))
print(len(ans)) """

# B
# AC
""" import math

for i in range(1,23333333):
    h = -i**2/23333333*math.log(i/23333333,2)-(23333333-i)**2/23333333*math.log((23333333-i)/23333333,2)
    if abs(h-11625907.5798) < 1e-4:
        print(i)
        break """

# C
# AC
""" strs = ""
for i in range(1,2024):
    strs += str(i)
a2 = 0
a20 = 0
a202 = 0
a2023 = 0
for i in strs:
    if i == "2":
        a2 += 1
        a202 += a20
    elif i == "0":
        a20 += a2
    elif i == "3":
        a2023 += a202
print(a2023) """

# D
# WA
""" from sympy import *
a = 47
b = 483031
count = 0
lis = []
x = 2
while x <= b:
    lis += [x**2]
    x = nextprime(x)
n = len(lis)
for i in range(n):
    for j in range(i):
        if 2333 < lis[i]+lis[j] < 233333333333:
            count += 1
print(count) """

# E
# AC
""" print(50*49*0.5-7*6*0.5) """

# F
# AC
""" from math import sqrt

w = 343720
h = 233333
for i in range(2,int(1e20),2):
    h2 = 233333*i
    w2 = h2/17*15
    if w2/w == int(w2/w) and int(w2/w)%2 == 0:
        print(sqrt(h2**2+w2**2))
        break """

# G
# AC
""" s = "kfdhtshmrw4nxg#f44ehlbn33ccto#mwfn2waebry#3qd1ubwyhcyuavuajb#vyecsycuzsmwp31ipzah#catatja3kaqbcss2th"
count = 0
for left in range(0,len(s)-16):
    for right in range(left+8,min(left+17,len(s))):
        tmp = s[left:right]
        if "#" in tmp and any(i in tmp for i in "0123456789"):
            count += 1
print(count) """

# H
# AC
""" from math import comb

for a in range(1,100):
    for b in range(1,100):
        for c in range(1,100):
            if a*b/comb(a+b+c,2) == 517/2091 and c*b/comb(a+b+c,2) == 2632/10455 and c*a/comb(a+b+c,2) == 308/2091:
                print(f"{a},{b},{c}")
                break """