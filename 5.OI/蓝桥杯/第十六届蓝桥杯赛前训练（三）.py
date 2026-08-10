# 第十六届蓝桥杯赛前训练（三） 模拟、二分
# A
# AC
""" H_list = [-50,-2,-3,-4,-5,-6,-7,-8,-9,-10,-20,-30,-40]
SD = [-100,100]

while True:
    players = []
    ans = []
    for _ in range(4):
        players += [input().split()[1:]]
    if not any(players):
        break
    for i in range(4):
        score = 0
        tmp = players[i]
        count = [0]*13
        count1 = [0,0]
        count2 = 0
        for j in tmp:
            if j[0] == "H":
                count[int(j[1:])-1] += 1
            if j == "S12":
                count1[0] += 1
            if j == "D11":
                count1[1] += 1
            if j == "C10":
                count2 += 1
        if all(count):
            score = 200
            if all(count1):
                score = 500
            else:
                for i in range(2):
                    score += count1[i]*SD[i] 
        else:
            for i in range(13):
                score += count[i]*H_list[i]
            for i in range(2):
                score += count1[i]*SD[i]
        if count2:
            if tmp == ["C10"]:
                score = 50
            else:
                score *= 2
        ans += [score]
    print(*["+"+str(i) if i > 0 else str(i) for i in ans]) """

# D
# AC
""" import math

m = int(input())
n = int(input())
num = []
sums = 0
for _ in range(m):
    a,b = map(int,input().split())
    num += [a*b]
    sums += a*b
mins = 1
maxs = max(num)
while mins < maxs:
    index = (mins + maxs)//2
    n1 = sum([math.ceil(i/index) for i in num])
    if n1 > n:
        mins = index + 1
    else:
        maxs = index
print(mins)
 """
# F
# AC
def canPlaceCows(positions, C, dist):
    count = 1
    last_position = positions[0]

    for i in range(1, len(positions)):
        if positions[i] - last_position >= dist:
            count += 1
            last_position = positions[i]
            if count == C:
                return True
    return False

def maxMinDistance(positions, C):
    positions.sort()

    low, high = 0, positions[-1] - positions[0]
    best_dist = 0

    while low < high:
        mid = (low + high + 1) // 2
        if canPlaceCows(positions, C, mid):
            best_dist = mid
            low = mid
        else:
            high = mid - 1

    return best_dist

N, C = map(int, input().split())
positions = [int(input()) for _ in range(N)]

print(maxMinDistance(positions, C))

