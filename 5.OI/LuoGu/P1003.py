n = int(input())
capture = []
for i in range(n):
    capture.append(list(map(int,input().split(" "))))
target = list(map(int,input().split(" ")))
def judge(k,i):return capture[i][k] <= target[k] <= (capture[i][k]+capture[i][k+2])
for i in range(len(capture))[::-1]:
    if judge(0,i) and judge(1,i):
        print(i+1)
        break
else:
    print("-1")
