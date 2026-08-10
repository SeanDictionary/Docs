d1,c,d2,p,n = map(float,input().split())
gassation = [[0,p]]
for _ in range(int(n)):
    gassation += [list(map(float,input().split()))]
gassation += [[d1,0]]
def costs(location,gas,cost):
    # 如果已经到终点就输出cost
    if location == n+1:
        print(f"{cost:.2f}")
        return 0
    tmp = gassation[location+1:]
    # 寻找比当前加油站便宜的，且能到达
    for distance,price in tmp:
        if price < gassation[location][1] and c*d2 >= distance - gassation[location][0]:
            return costs(gassation.index([distance,price]),0,cost+((distance - gassation[location][0])/d2-gas)*gassation[location][1])
    cur_d,cur_p = float("inf"),float("inf")
    # 寻找能到达的最便宜的加油站
    for distance,price in tmp:
        if c*d2 >= distance - gassation[location][0] and price < cur_p:
            cur_d = distance
            cur_p = price
    # 如果找不到意味着没有能到达的下一个站
    if cur_p == float("inf"):
        print("No Solution")
        return 0
    return costs(gassation.index([cur_d,cur_p]),c-(cur_d - gassation[location][0])/d2,cost+(c-gas)*gassation[location][1])

costs(0,0,0)
