n = int(input())
output = []
for _ in range(n):
    output += [input().split()]
alpha = output[0][1:]
ans = {}
for i in output[1:]:
    count = 0
    for j in i[1:]:
        if len(j) == 2:
            count += 1
    ans[i[0]] = count
ans_reverse = {item:key for key,item in ans.items()}
res = []
res += [["+"]+alpha]
for i in range(n-1):
    tmp = [alpha[i]]
    for j in range(n-1):
        a = (ans[alpha[i]]+ans[alpha[j]])
        if a//(n-1) == 0:
            tmp += [ans_reverse[a]]
        else:
            tmp += [ans_reverse[a//(n-1)]+ans_reverse[a%(n-1)]]
    res += [tmp]
if res == output:
    print(" ".join(f"{key}={item}" for key, item in ans.items()))
    print(n-1)
else:
    print("ERROR!")