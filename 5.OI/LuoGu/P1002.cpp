#include<iostream>
#include<cstring>
#define ll long long
using namespace std;
ll dp[22][22];
int main(){
    int bx,by,mx,my;
    cin >> bx >> by >> mx >> my;
    bx += 1; by += 1; mx += 1; my += 1;
    memset(dp, 0, sizeof(dp));
    for (int x = 1; x <= bx; x++){
        for (int y = 1; y<= by; y++){
            if (abs(x - mx) == 1 && abs(y - my) == 2 || abs(x - mx) == 2 && abs(y - my) == 1 || x == mx && y == my){
                dp[x][y] = 0;
            }
            else if (x == 1 && y == 1){
                dp[x][y] = 1;
            }
            else{
                dp[x][y] = dp[x-1][y] + dp[x][y-1];
            }
        }
    }
    // 用于输出调试
    // for (int i = 0; i <= bx; i++) {
    //     for (int j = 0; j <= by; j++) {
    //         cout << dp[i][j] << " "; 
    //     }
    //     cout << endl;
    // }
    cout << dp[bx][by];
}