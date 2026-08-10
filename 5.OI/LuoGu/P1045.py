import numpy as np
n = int(input())
a = int(np.log10(2)*n+1)
b = pow(2,n,10**500)-1
last = f"{str(b):0>500}"
ans = [last[i:i+50] for i in range(0,500,50)]
print(a)
print("\n".join(ans))