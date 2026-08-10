n = int(input())
sum = 0
i = 2
while True:
    sum += i
    if sum > n:
        sum -= i
        i -= 1
        break
    i += 1
lis = [i for i in range(2,i+1)]
for i in range(i-2,i-2-(n-sum),-1):
    lis[i]+=1
ans = 1
for i in lis:
    ans *= i
print(*lis)
print(ans)