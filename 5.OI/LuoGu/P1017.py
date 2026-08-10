n,R = map(int,input().split())
alpha = "0123456789ABCDEFGHIJ"

def change(n,R):
    ans = ""
    while not 0 < n < abs(R):
        ans += alpha[n%abs(R)]
        n = (n-n%abs(R))//R
    ans += alpha[n]
    return ans[::-1]

print(f"{n}={change(n,R)}(base{R})")