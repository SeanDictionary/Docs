# L2-1
n = int(input())
lis = []
for _ in range(n):
    lis += [list(map(int,input().split()))]
lis.sort(key=lambda x:(x[0],x[1],x[2],x[3]))
same = [0,0,0,0]
count = 0
sign = 1
for i in lis:
    if i == same:
        sign += 1
        if sign == 3:
            count += 1
    else:
        sign = 1
        same = i
print(count)