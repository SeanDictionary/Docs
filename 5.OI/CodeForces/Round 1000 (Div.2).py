# Round 1000 (Div.2)
# 25/01/22
# A
# AC
""" t = int(input())
for _ in range(t):
    a,b = map(int,input().split())
    print(1 if a == 1 and b == a else b-a) """

# B
# AC
""" t = int(input())
for _ in range(t):
    n,l,r = map(int,input().split())
    lis = list(map(int,input().split()))
    left = sorted(lis[:r])
    right = sorted(lis[l-1:])
    print(min(sum(left[:r-l+1]),sum(right[:r-l+1]))) """

# C
# AC
def max_nodes(tree:dict):
    maxs = 0
    nodes = []
    for value in tree.values():
        if len(value) > maxs:
            maxs = len(value)
    for key,value in tree.items():
        if len(value) == maxs:
            nodes += [key]
    return nodes,maxs

t = int(input())
for _ in range(t):
    n = int(input())
    tree = {}
    for _ in range(n-1):
        x,y = map(int,input().split())
        if x not in tree:
            tree[x] = {y}
        else:
            tree[x].add(y)
        if y not in tree:
            tree[y] = {x}
        else:
            tree[y].add(x)

    nodes,max1 = max_nodes(tree)
    # 这里直接对最多节点数的节点先行输出了
    if len(nodes) == 2:
        if nodes[1] in tree[nodes[0]]:
            print(2*max1-2)
        else:
            print(2*max1-1)
    elif len(nodes) > 2:
        print(2*max1-1)
    # 只有最多节点数只有一个的时候，要遍历其余的节点算最大值
    # 此时就只有O(n)了
    else:
        max2 = 0
        for i in tree[nodes[0]]:
            tree[i].discard(nodes[0])
        nodesss = tree.pop(nodes[0])
        
        max2 = max(max_nodes(tree)[1],max2)
        print(max2+max1-1)