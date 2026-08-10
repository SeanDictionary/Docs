# Misc

## wireshark

### 1. 题目分析

题目提供了一个抓包文件：

```
challenge.pcapng
```

初步判断这是一个 **流量分析题（Network Forensics）**。

使用 Wireshark 打开抓包文件，查看协议层级：

```
Statistics → Protocol Hierarchy
```

可以看到大量：

```
TCP
 └── Modbus/TCP
```

说明本题与 **工控协议 Modbus** 有关。

---

## 2. Modbus/TCP 协议结构

Modbus/TCP 数据包结构如下：

```
MBAP Header (7 bytes)

Transaction ID   2 bytes
Protocol ID      2 bytes
Length           2 bytes
Unit ID          1 byte

PDU
Function Code    1 byte
Data             n bytes
```

关键字段：

```
Function Code
```

它表示 Modbus 操作类型。

常见功能码：

| Function Code | 含义                     |
| ------------- | ------------------------ |
| 1             | Read Coils               |
| 3             | Read Holding Registers   |
| 5             | Write Single Coil        |
| 16            | Write Multiple Registers |
| 8             | Diagnostics              |

其中 **Function Code = 8（Diagnostics）** 在正常工业通信中很少使用，因此可能被用于隐藏数据。

---

## 3. 流量特征分析

在 Wireshark 中使用过滤器：

```
tcp.port == 502
```

可以筛选出 Modbus 流量。

进一步观察发现：

```
Source IP      : 192.168.100.10
Destination IP : 192.168.100.101
Port           : 502
Function Code  : 8
```

同时：

```
Unit ID = 5
Unit ID = 7
```

说明这些包很可能是 **攻击者构造的隐藏通信**。

---

## 4. 隐藏数据结构

继续分析这些包的 PDU 部分：

```
Function Code = 8
Subfunction   = 2 bytes
Data          = 8 bytes
```

发现：

```
payload 长度固定为 8 bytes
```

这非常关键，因为：

```
DES block size = 8 bytes
```

说明：

**每个 Modbus 包中可能隐藏了一个 DES 密文块。**

---

## 5. 数据提取思路

提取条件：

```
src = 192.168.100.10
dst = 192.168.100.101
port = 502
Function Code = 8
Unit ID = 5 或 7
payload 长度 = 8 bytes
```

将所有 payload 按时间排序后拼接：

```
ciphertext =
block1 + block2 + block3 + ...
```

得到完整 DES 密文。

---

## 6. DES 解密

题目中使用 DES 加密：

```
key = S7COMM01
mode = ECB
```

DES 参数：

```
block size = 8 bytes
key size   = 8 bytes
mode       = ECB
```

解密后再去除 PKCS7 padding。

---

## 7. 解题脚本

```python
from Crypto.Cipher import DES
from scapy.all import IP, TCP, Raw, PcapNgReader


PCAP_FILE = "challenge.pcapng"
MASTER_IP = "192.168.100.10"
SLAVE_IP = "192.168.100.101"
DES_KEY = "S7COMM01"


def parse(pcap_path: str):
    for idx, pkt in enumerate(PcapNgReader(pcap_path), start=1):

        if IP not in pkt or TCP not in pkt or Raw not in pkt:
            continue

        ip = pkt[IP]
        tcp = pkt[TCP]
        data = bytes(pkt[Raw].load)

        if len(data) < 8:
            continue

        if data[2:4] != b"\x00\x00":
            continue

        mbap_len = int.from_bytes(data[4:6], "big")

        if mbap_len + 6 != len(data):
            continue

        yield idx, float(pkt.time), ip.src, ip.dst, tcp.sport, tcp.dport, data


def get(modbus_stream):

    chunks = []

    for row in modbus_stream:
        idx, ts, src, dst, sport, dport, data = row
        if (src == MASTER_IP and dst == SLAVE_IP and dport == 502) and data[7] == 8 and data[6] in (5, 7) and len(data) >= 18:
            subfunc = int.from_bytes(data[8:10], "big")
            payload = data[10:]
            if subfunc != 0 or len(payload) != 8:
                continue
            chunks.append((idx, ts, data[6], payload))

    return chunks


modbus_stream = list(parse(PCAP_FILE))
key = DES_KEY.encode()
chunks = get(modbus_stream)
ciphertext = b"".join(x[3] for x in sorted(chunks, key=lambda r: r[1]))
result = DES.new(key, DES.MODE_ECB).decrypt(ciphertext)
print(result)
```

得到flag：flag{d3f8e2d1-7c19-4a6b-b5e8-9d2f0c4a7e31}\x06\x06\x06\x06\x06\x06
