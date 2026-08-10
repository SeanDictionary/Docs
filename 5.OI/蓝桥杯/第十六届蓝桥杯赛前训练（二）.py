# 第十六届蓝桥杯赛前训练（二）枚举、贪心
# 24/12/13
# T1
# AC
""" n = input().split("boo")
print("hu".join(n)) """

# T2
# AC
""" import sys
sys.set_int_max_str_digits(0)

n = int(input())
for _ in range(n):
    m = input()
    count2 = m.count("2")
    count3 = m.count("3")
    m = int(m)%9
    sign = 0
    i,j = 0,0
    while not sign:
        if j > count3:
            j = 0
            i += 1
            if i > count2:
                break
        if (i * 2 + j * 6 + m) % 9 == 0:
            sign = 1
        j += 1
    if sign:
        print("YES")
    else:
        print("NO") """

# T3
# RE
""" t = int(input())
for _ in range(t):
    n = [i for i in input()]
    while True:
        sign = 1
        for i in range(1,len(n)):
            if int(n[i]) > int(n[i-1]) + 1:
                tmp = n[i-1]
                n[i-1] = str(int(n[i]) - 1)
                n[i] = tmp
                sign = 0
        if sign:
            break
    print("".join(n)) """

# AC(C++)
""" #include <iostream>
#include <vector>
#include <string>

int main() {
	int t;
	std::cin >> t;
	while (t--) {
		std::string input;
		std::cin >> input;
		std::vector<int> n(input.begin(), input.end());
		for (auto& c : n) c -= '0'; // Convert char to int

		while (true) {
			bool sign = true;
			for (size_t i = 1; i < n.size(); ++i) {
				if (n[i] > n[i - 1] + 1) {
					int tmp = n[i - 1];
					n[i - 1] = n[i] - 1;
					n[i] = tmp;
					sign = false;
				}
			}
			if (sign) break;
		}

		for (const auto& num : n) {
			std::cout << num;
		}
		std::cout << std::endl;
	}
	return 0;
} """

# T4
# WA
""" n,k = map(int,input().split())
tmp = list(map(int,input().split()))
l = []
for i in range(1,len(tmp)):
    l.append(tmp[i]-tmp[i-1])
if len(l)%2 == 1:
    print(sum([l[i] for i in range(0,len(l),2)]))
elif len(l) == 0:
    print(0)
else:
    tmp1 = [l[0],l[1]]
    for i in range(2,len(l)):
        tmp1.append(tmp1[-2]+l[i])
    tmp1.pop(-1)
    tmp2 = [l[-1],l[-2]]
    for i in range(len(l)-3,-1,-1):
        tmp2.append(tmp2[-2]+l[i])
    tmp2.pop(-1)
    tmp2 = tmp2[::-1]
    mins = float("inf")
    for i in range(len(tmp1)-2):
        if i%2 == 0:
            mins = min(mins,tmp1[i]+tmp2[i+2])
        else:
            mins = min(mins,tmp1[i-1]+tmp2[i+3]+l[i+1]+l[i+2])
    print(mins) """

# T6
# AC
""" t = int(input())
for _ in range(t):
    n,m,k = map(int,input().split())
    tmp = input()+"L"
    now = -1
    sign = 1
    while now < n and sign:
        if tmp[now+1] == "L" and m > 0:
            now += 1
        else:
            for i in range(1,m+1):
                if tmp[now+i] == "L":
                    now += i
                    break
            else:
                for i in range(k+1):
                    if tmp[now+m+i] == "C":
                        sign = 0
                        break
                    elif tmp[now+m+i] == "L":
                        k -= i
                        now += m+i
                        break
                else:
                    sign = 0
    if sign:
        print("YES")
    else:
        print("NO") """