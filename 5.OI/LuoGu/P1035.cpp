#include<bits/stdc++.h>
#define endl "\n"
using namespace std;
int main(){
    long long ans = 0;
    int k;
    cin >> k;
    long double sum = 0;
    while(sum <= k){
        ans += 1;
        sum += 1.0*1/ans;
    }
    cout << ans << endl;
}