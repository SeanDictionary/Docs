#include<bits/stdc++.h>
#define endl "\n"
#define ll long long
using namespace std;

#define MOD ((ll)1e9+7)
#define MAX (ll)1e4

int nums[MAX];

int main(){
    ll ans = 0, maxs = 0,n;
    cin >> n;
    for (int i = 0; i < n; i++){
        ll l;
        cin >> l;
        nums[l] += 1;
        maxs = max(l,maxs);
    }
    for (int i = 2; i <= maxs; i++){
        if (nums[i] >= 2){
            for (int x = 1; x <= i/2; x++){
                int y = i-x;
                if (y == x){
                    ans = (ans + nums[x]*(nums[x]-1)/2*nums[i]*(nums[i]-1)/2)%MOD;
                }
                else{
                    ans = (ans + nums[x]*nums[y]*nums[i]*(nums[i]-1)/2)%MOD;
                }
            }
        }
    }
    cout << ans << endl;
}