#include<bits/stdc++.h>
#define endl "\n"
using namespace std;

#define MAX 510

int main(){
    string a, b;
    int na[MAX] = {0}, nb[MAX] = {0};
    cin >> a >> b;
    for (int i = 0; i < a.size(); i++) na[i] = a[a.size()-i-1] - '0';
    for (int i = 0; i < b.size(); i++) nb[i] = b[b.size()-i-1] - '0';
    int max_lenth = max(a.size(), b.size());
    int jinwei = 0;
    for (int i = 0; i < max_lenth; i++){
        int tmp = na[i] + nb[i] + jinwei;
        na[i] = tmp%10;
        jinwei = tmp/10;
    }
    na[max_lenth] = jinwei;
    while (!na[max_lenth]) max_lenth -= 1;
    if (max_lenth == -1){
        cout << '0';
    }
    for (int i = max_lenth; i >= 0; i--) cout << na[i];
}