#include <bits/stdc++.h>
using namespace std;

int lis[100];

int main(){
	int n, k;
	int max1 = 0, max2 = 0;
	int index1 = 0, index2 = 0;
	cin >> n >> k;
	for (int i = 0; i < n; i++){
		int x;
		for (int j = 0; j < k; j++){
			cin >> x;
			lis[i] += x;
		}
		if (lis[i] > max1) {max2 = max1; index2 = index1;max1 = lis[i]; index1 = i;}
		else if (lis[i] > max2) {max2 = lis[i]; index2 = i;}
	}
	cout << index1+1 << "\n" << index2+1 << endl;
	return 0;
}
