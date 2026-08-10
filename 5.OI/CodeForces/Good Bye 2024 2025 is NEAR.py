# Good Bye 2024: 2025 is NEAR
# 24/12/28
# A
# AC
""" t = int(input())
for _ in range(t):
    n = int(input())
    lis = list(map(int,input().split()))
    for i in range(1,n):
        a = max(lis[i-1],lis[i])
        b = min(lis[i-1],lis[i])
        if a/2 < b:
            print("YES")
            break
    else:
        print("NO") """

# B
# Python TLE
""" t = int(input())
for _ in range(t):
    n = int(input())
    a = [0]*(2*n+1)
    lis = []
    ans = ""
    for _ in range(n):
        x = list(map(int,input().split()))
        lis += [x]
        if x[0] == x[1]:
            a[x[0]] += 1
    sums = [0]*(2*n+1)
    for i in range(1,2*n+1):
        x = 1 if a[i] > 0 else 0
        sums[i] = x + sums[i-1]
    for i in range(n):
        l = lis[i][1]-lis[i][0]+1
        if l == 1:
            if a[lis[i][0]] == 1:
                ans += "1"
            else:
                ans += "0"
        else:
            if l > sums[lis[i][1]]-sums[lis[i][0]-1]:
                ans += "1"
            else:
                ans += "0"
    print(ans)
 """
# C++ AC
#include <iostream>
#include <vector>
""" using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(2 * n + 1, 0);
        vector<vector<int>> lis;
        string ans = "";
        for (int i = 0; i < n; ++i) {
            int x, y;
            cin >> x >> y;
            lis.push_back({x, y});
            if (x == y) {
                a[x]++;
            }
        }
        vector<int> sums(2 * n + 1, 0);
        for (int i = 1; i <= 2 * n; ++i) {
            int x = a[i] > 0 ? 1 : 0;
            sums[i] = x + sums[i - 1];
        }
        for (int i = 0; i < n; ++i) {
            int l = lis[i][1] - lis[i][0] + 1;
            if (l == 1) {
                if (a[lis[i][0]] == 1) {
                    ans += "1";
                } else {
                    ans += "0";
                }
            } else {
                if (l > sums[lis[i][1]] - sums[lis[i][0] - 1]) {
                    ans += "1";
                } else {
                    ans += "0";
                }
            }
        }
        cout << ans << endl;
    }
    return 0;
} """

# C
# TLE
# 二维dp不行
""" t = int(input())
for _ in range(t):
    n,k = map(int,input().split())
    dp = [[0]*n for _ in range(n)]
    for lenth in range(k,n+1):
        for l in range(n-lenth+1):
            r = lenth + l - 1
            if lenth%2 != 0:
                mid = (l+r)//2
                dp[l][r] = mid+1 + dp[l][mid-1] + dp[mid+1][r]
            else:
                mid = (l+r)//2
                dp[l][r] = dp[l][mid] + dp[mid+1][r]
    print(dp[0][-1]) """

# TLE
# 一维dp
t = int(input())
for _ in range(t):
    n,k = map(int,input().split())
    dp = [0]+[0]*n
    for i in range(k,n+1):
        times = 0
        a = i
        b = 1
        while a >= k:
            if a%2 != 0:
                times += b
            b *= 2
            a //= 2
        if i%2 != 0:
            dp[i] = (i+1)//2 + 2*dp[i//2] + (times-1)//2*(i//2+1)
        else:
            dp[i] = 2*dp[i//2] + times//2*(i//2)
    print(dp[-1])
