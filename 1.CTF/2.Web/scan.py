import subprocess

output = "./known_hosts.txt"
IP = "192.168.101.1"
tmp = IP.split(".")[-1]
target = ".".join(IP.split(".")[:-1])

for x in range(1, 255):
    if x == int(tmp):
        continue
    host = f"{target}.{x}"
    try:
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "500", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            continue

        print(f"{host}")
        with open(output, "a") as f:
            f.write(f"{host}\n")
    except Exception:
        pass
