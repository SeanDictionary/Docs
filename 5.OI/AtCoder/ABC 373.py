# ABC 373
# 24/9/28
# T1
""" def solution(strs):
    ans = 0
    for n,i in enumerate(strs):
        if len(i) == n+1:
            ans += 1
    return ans

strs = [input()for _ in range(12)]
print(solution(strs)) """

# T2
""" def solution(strs):
    mem = {}
    ans = 0
    for n,i in enumerate(strs):
        mem[i] = n
    for x in range(65,90):
        ans += abs(mem[chr(x)]-mem[chr(x+1)])
    return ans
strs = input()
print(solution(strs)) """

# T3
""" def solution(num1,num2,n):
    a1=a2=float('-inf')
    for i in range(n):
        a1 = max(a1,int(num1[i]))
        a2 = max(a2,int(num2[i]))
    return a1+a2

n = int(input())
num1 = input().split()
num2 = input().split()
print(solution(num1,num2,n)) """
