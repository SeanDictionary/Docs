#include <bits/stdc++.h>
#define ll long long
#define space " "
#define endl "\n"
using namespace std;

#define MAX 541

int multiply(int ans[], int a, int index){
    for (int i = 0; i <= index; i++){
        ans[i] *= a;
    }
    for (int i = 0; i < MAX-1; i++){
        ans[i+1] += ans[i]/10;
        ans[i] %= 10;
    }
    for (int i = MAX-1; i >= 0; i--){
        if(ans[i] != 0) {
            return i;
        }
    }
}

int main(){
    ll n;
    cin >> n;
    ll i=2, sum=0;
    while(1){
        sum += i;
        if(sum<=n){
            i++;
        }
        else{
            sum -= i;
            break;
        }
    }
    i--;
    int ans[MAX] = {1};
    int index = 0;
    int lis[i-1] = {0};
    for(int k = 0; k < i-1; k++) lis[k] = k+2;
    for(int k = i-2; k >= (i-1-(n-sum)<0 ? 0 : i-1-(n-sum)); k--) lis[k] += 1;
    if(i-1-(n-sum)<0)lis[i-2]+=1;
    for(int k = 0; k < i-1; k++){
        index = multiply(ans, lis[k], index);
        cout << lis[k] << space;
    }
    cout << endl;
    for(int k = index; k >= 0; k--) cout << ans[k];
}