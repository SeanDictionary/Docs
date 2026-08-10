def a(n):
    if n in mem:
        return mem[n]
    tmp = bin(n)[2:]
    res = []    
    for i in range(-len(tmp),0):
        if tmp[i] == "1":
            if i != -2:
                res += [f"2({a(-i-1)})"]
            else:
                res += ["2"]
    mem[n] = "+".join(res)
    return mem[n]

mem = {0:"0", 1:"2(0)", 2:"2"}
n = int(input())
print(a(n))