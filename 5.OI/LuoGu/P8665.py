class Time:
    def __init__(self,times:str):
        times = times.split(":")
        seconds = (int(times[0])*60+int(times[1]))*60+int(times[2])
        self.seconds = seconds  
        self.s = seconds%60
        self.m = seconds//60%60
        self.h = seconds//60//60
    def __str__ (self):
        return (f"{self.h:02d}:{self.m:02d}:{self.s:02d}")
    def __add__(self,other:"Time"):
        s = self.s + other.s
        m = self.m + other.m
        h = self.h + other.h
        return (Time(f"{h:02d}:{m:02d}:{s:02d}"))
    def __sub__(self,other:"Time"):
        h = self.h - other.h
        m = self.m - other.m
        s = self.s - other.s
        return (Time(f"{h:02d}:{m:02d}:{s:02d}"))
    def __mul__(self,n:int):
        s = self.s*n
        m = self.m*n
        h = self.h*n
        return (Time(f"{h:02d}:{m:02d}:{s:02d}"))
    def __floordiv__(self,n:int):
        seconds = self.seconds//n
        s = seconds%60
        m = seconds//60%60
        h = seconds//60//60
        return (Time(f"{h:02d}:{m:02d}:{s:02d}"))

n = int(input())
ans = []
for _ in range(n):
    tmp1 = input().split()
    tmp1[0],tmp1[1] = map(Time,tmp1[:2])
    if len(tmp1) == 3:
        tmp1[1] += Time("24:00:00")*int(tmp1[2][2])
    tmp2 = input().split()
    tmp2[0],tmp2[1] = map(Time,tmp2[:2])
    if len(tmp2) == 3:
        tmp2[1] += Time("24:00:00")*int(tmp2[2][2])
    ans += [(tmp1[1]-tmp1[0]+tmp2[1]-tmp2[0])//2]
print("\n".join(str(i) for i in ans))