n = int(input())
ans = 0
s = 0
while s <= n:
    ans += 1
    s += 1/ans
print(ans)