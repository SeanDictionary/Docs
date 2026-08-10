n = int(input())
delta = pow((1/4+2*n),0.5)
m = int(-0.5+delta) if int(-0.5+delta) == -0.5+delta else int(-0.5+delta)+1
position = n - ((m-1)**2+(m-1))//2
if m%2 == 0:
    print(f"{position}/{m+1-position}")
else:
    print(f"{m+1-position}/{position}")