# 24/12/1

# CACC T1
# 约瑟夫问题
# 暴力模拟
# 10/10 AC
n, k = map(int,input().split())
lis = [i+1 for i in range(n)]
count = n-1
num = 1
index = 0
while any(lis) and count:
    if num%k == 0:
        lis[index%n] = 0
        count -= 1
    num += 1
    index += 1
    while not lis[index%n]:
        index += 1
print(sum(lis))

# CACC T2
# 数据预处理最大值
# 10/10 AC

# CACC T3
# 考场上7/10 WA 3/10 TLE
n, m = map(int,input().split())
num = [0] * n
for _ in range(n):
    action = list(map(int,input().split()))
    if action[0] == 1:
        for i in range(action[1]-1, action[2]):
            if num[i]%2 == action[3]:
                num[i] += action[4]
    else:
        print(sum(num[action[1]-1:action[2]]))

# CACC T5
# 126/200 分
class Scheduler():
    def __init__(self):
        pass

    def init(self, n, c, m):
        self.n = n
        self.total_vcpu = c
        self.total_mem = m
        self.physical = {i:[c,m] for i in range(n)} # 记录物理机状态
        self.vm_nums = {}       # 记录虚拟机状态

    def create(self, id, c, m):
        mins, num = float("inf"), -1
        expand = 0
        for i in range(self.n):
            percent_vcpu = (self.physical[i][0] - c)/self.total_vcpu    # 计算剩余核心占比
            percent_mem = (self.physical[i][1] - m)/self.total_mem      # 计算剩余内存占比
            if percent_vcpu + percent_mem < mins and percent_mem >= 0 and percent_vcpu >= 0:
                mins = percent_vcpu + percent_mem
                num = i
        if num == -1:    # 意味没有满足条件的物理机，要扩容
            expand = 1
            num = self.n
            self.physical[self.n] = [self.total_vcpu - c, self.total_mem - m]
            self.vm_nums[id] = [self.n, c, m]
            self.n += 1
        else:
            self.physical[num][0] -= c
            self.physical[num][1] -= m
            self.vm_nums[id] = [num, c, m]

        return (num, expand)
    
    def remove(self,id):
        num, c, m = self.vm_nums[id]    # 读取虚拟机信息
        self.physical[num][0] += c  # 恢复物理机状态
        self.physical[num][1] += m
        del(self.vm_nums[id])   # 删除虚拟机信息

def debug(action, tuple:tuple): # 调试用，源代码没有
    try:
        if action == "init":
            machine.init(*tuple)
        elif action == "create":
            machine.create(*tuple)
        elif action == "remove":
            machine.remove(tuple)
        print(f"[+] {action.upper():6} : PM {machine.physical}")
        print(f"[+]        : VM {machine.vm_nums}")
    except Exception as error:
        print(f"[-] ERROR  : {error}")

machine = Scheduler()
debug("init",(1,32,128))
debug("create",(1,16,64))
debug("create",(2,32,64))
debug("remove",(2))
debug("create",(3,32,64))

# [+] INIT   : PM {0: [32, 128]}
# [+]        : VM {}
# [+] CREATE : PM {0: [16, 64]}
# [+]        : VM {1: [0, 16, 64]}
# [+] CREATE : PM {0: [16, 64], 1: [0, 64]}
# [+]        : VM {1: [0, 16, 64], 2: [1, 32, 64]}
# [+] REMOVE : PM {0: [16, 64], 1: [32, 128]}
# [+]        : VM {1: [0, 16, 64]}
# [+] CREATE : PM {0: [16, 64], 1: [0, 64]}
# [+]        : VM {1: [0, 16, 64], 3: [1, 32, 64]}