n = int(input())
m = input()
alpha = "0123456789ABCDEF"
def change(m,n):
    ans = ""
    while m//n != 0:
        ans += alpha[m%n]
        m = m//n
    ans += alpha[m%n]
    return ans

for i in range(1,31):
    m = change(int(m,n)+int(m[::-1],n),n)
    if m == m[::-1]:
        print(f"STEP={i}")
        break
else:
    print("Impossible!")