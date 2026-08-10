b_x, b_y, m_x, m_y = map(int,input().split(" "))
dp = [[0]*(b_x+2) for _ in range(b_y+2)] # 生成比标准格子大一圈

# 判断是否在控制点上
def a(x,y):
    return abs(m_x-x+1) == 1 and abs(m_y-y+1) == 2 or abs(m_x-x+1) == 2 and abs(m_y-y+1) == 1 or (m_x+1) == x and (m_y+1) == y

for y in range(1,b_y+2):
    for x in range(1,b_x+2):
        if x == 1 and y == 1:
            dp[y][x] = 1 # 初始点
        else:
            if a(x,y):
                dp[y][x] = 0    # 控制点为0
            else:
                dp[y][x] = dp[y][x-1]+dp[y-1][x] # 上左格子和
print(dp[-1][-1])