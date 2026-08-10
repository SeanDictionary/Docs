for i in range(192,330):
    if "0" in str(i)+str(i*2)+str(i*3):
        continue
    alpha = {"1":1, "2":1, "3":1, "4":1, "5":1, "6":1, "7":1, "8":1, "9":1}
    for j in str(i)+str(i*2)+str(i*3):
        if alpha[j] == 1:
            alpha[j] = 0
        else:
            break
    else:
        print(f"{i} {i*2} {i*3}")
