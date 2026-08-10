target = "1011111110000000110110001110011000111111111011110011111111000010"
def dfs(stream,output,index):
    global ans
    if stream[-1] == "1":
        index += 1
    tmp = stream[index] if index != -1 else "1"
    if output+tmp == target[:len(output)+1]:
        if len(stream) == len(target):
            ans += [stream]
        else:
            dfs(stream+"0",output+tmp,index)
            dfs(stream+"1",output+tmp,index)
 
stream = "0"
ans = []
dfs(stream,"",-1)
with open("output.txt","w") as f:
    for i in ans:
        f.write(i+"\n")




