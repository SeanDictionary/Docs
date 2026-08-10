# 24/12/7
# ABC 383
# T1
# AC
""" n = int(input())
time = 0
all = 0
for _ in range(n):
    t, l = map(int,input().split())
    all = all - (t - time) if all - (t - time) >= 0 else 0
    time = t
    all += l
print(all) """

# T2
# AC
""" h, w, d = map(int,input().split())
lis = []
for _ in range(h):
    lis += [[0 if i == "#" else 1 for i in input()]]
ans = 0
for x1 in range(h):
    for y1 in range(w):
        if lis[x1][y1] == 1:
            for x2 in range(h):
                for y2 in range(w):
                    if lis[x2][y2] == 1:
                        count = 0
                        for x in range(h):
                            for y in range(w):
                                if lis[x][y] == 1 and (abs(x-x1) + abs(y-y1) <= d or abs(x-x2) + abs(y-y2) <= d):
                                    count += 1
                        ans = max(ans, count)
print(ans) """

# T3
# TLE
""" h, w, d = map(int,input().split())
lis = [[0]*(w+2)]
for _ in range(h):
    lis += [[0]+[0 if i == "#" else 1 if i == "." else 2 for i in input()]+[0]]
lis += [[0]*(w+2)]
ans = 0

def dfs(x,y,d):
    sets = set()
    if d == 0:
        return {(x,y)}
    else:
        if lis[x-1][y] != 0:
            sets.add((x-1,y))
            sets.update(dfs(x-1,y,d-1))
        if lis[x][y-1] != 0:
            sets.add((x,y-1))
            sets.update(dfs(x,y-1,d-1))
        if lis[x][y+1] != 0:
            sets.add((x,y+1))
            sets.update(dfs(x,y+1,d-1))
        if lis[x+1][y] != 0:
            sets.add((x+1,y))
            sets.update(dfs(x+1,y,d-1))
    return sets

ans = set()
for x in range(1,h+1):
    for y in range(1,w+1):
        if lis[x][y] == 2:
            ans.add((x,y))
            ans.update(dfs(x,y,d))
print(len(ans)) """

# T4
# WA
""" n = int(input())
lis = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321, 1327, 1361, 1367, 1373, 1381, 1399, 1409]
nums = 0
for i in range(len(lis)):
    if lis[i]**2 * 4 > n:
        break
    nums = sum([x for x in range(i+1,0,-2)])
for i in range(len(lis)):
    if lis[i]**8 <= n:
        nums += 1
    else:
        break
print(nums) """