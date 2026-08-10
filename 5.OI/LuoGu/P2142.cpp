#include<bits/stdc++.h>
#define endl "\n"
#define MAX 10500
using namespace std;

int judge(string a, string b){
    if (a.size() < b.size()) return 1;
    if (a.size() > b.size()) return 0;
    for (int i = a.size()-1; i >= 0; i--){
        if (a[i] != b[i]){
            return a[i] < b[i];
        }
    }
    return 0;
}

int main(){
    string a, b;
    int na[MAX] = {0}, nb[MAX] = {0};
    cin >> a >> b;
    if (a != b){
        if (judge(a,b)){
            string x = a;
            a = b;
            b = x;
            cout << "-";
        }
        for (int i = 0; i < a.size(); i++) na[i] = a[a.size()-i-1] - '0';
        for (int i = 0; i < b.size(); i++) nb[i] = b[b.size()-i-1] - '0';
        int max_lenth = max(a.size(), b.size());
        int jinwei = 0;
        for (int i = 0; i < max_lenth; i++){
            if (na[i] - jinwei >= nb[i]) {
                na[i] = na[i] - jinwei - nb[i];
                jinwei = 0;
            }
            else{
                na[i] = na[i] - jinwei - nb[i] + 10;
                jinwei = 1;
            }
        }
        while (!na[max_lenth - 1]) max_lenth -= 1;
        for (int i = max_lenth - 1; i >= 0; i--) cout << na[i];
    }
    else cout << 0;
}