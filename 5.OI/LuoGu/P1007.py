l = int(input())
n = int(input())
if n != 0:
    x = list(map(int,input().split()))
    mins = max([min(l-i+1,i) for i in x])
    maxs = max([max(l-i+1,i) for i in x])
    print(f"{mins} {maxs}")
else:
    print("0 0")