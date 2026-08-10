#include<bits/stdc++.h>
#define endl "\n"
using namespace std;

#define MAX 10001

int main(){
    string a, b;
    int na[MAX] = {0}, nb[MAX] = {0}, ans[MAX] = {0};
    cin >> a >> b;
    for (int i = 0; i < a.size(); i++) na[i] = a[a.size()-i-1] - '0';
    for (int i = 0; i < b.size(); i++) nb[i] = b[b.size()-i-1] - '0';
    for (int i = 0; i < a.size(); i++){
        for (int j = 0; j < b.size(); j++){
            ans[i+j] += na[i] * nb[j];
        }
    }
    int max_lenth = a.size() + b.size();
    int jinwei = 0;
    for (int i = 0; i < max_lenth; i++){
        ans[i+1] += ans[i]/10;
        ans[i] = ans[i]%10;
    }
    while (!ans[max_lenth]) {
        max_lenth -= 1;
        if (max_lenth == -1) {
            cout << '0'; break;
        }
    }
    for (int i = max_lenth; i >= 0; i--) cout << ans[i];
}