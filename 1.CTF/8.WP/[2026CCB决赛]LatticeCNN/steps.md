## Session 2026-04-28

### Step 1
- Category / Skill: `ctf-solver`
- Fact: 题目目录只有 `task/task.py`、`task/inputs.npy`、`task/outputs.npy`、`task/public.json`、`task/cipher.bin`。`task.py` 中公开了两层卷积核、ReLU、2x2 平均池化、8x8 混合矩阵 `MIX`、模数 `q=65537`、噪声界 `2`，输出形如 `b_i = <a_i, s> + e_i (mod q)`。
- Inference: 这是一个把 CNN-like 特征抽取包装成 LWE/带小噪声线性同余恢复的问题，优先从 `ctf-solver` 路由到 `ctf-crypto`。
- Next Action: 复现 `feature(x)`，从 `inputs.npy` 生成公开矩阵 `A`，验证方程组规模和秩。
- Command / Payload / Operation: 阅读 `task/task.py`、`task/public.json`，并用临时 Python 复算输入输出维度。
- Key Result: `inputs.npy` 形状为 `(24, 6, 6)`，`outputs.npy` 形状为 `(24,)`，`cipher.bin` 大小为 `48` 字节。
- Why It Matters: 先把题型钉死，避免误走成“需要训练模型”或“需要逆神经网络”的错误方向。

### Step 2
- Category / Skill: `ctf-crypto`
- Fact: 根据公开卷积核、池化和 `MIX`，可从每个输入样本稳定生成 8 维向量 `a_i`；拼成矩阵后 `A` 的形状为 `24x8`，整数域数值秩为 `8`。
- Inference: 秘密向量 `s` 维度为 `8`，且样本数足以恢复；难点仅在每个方程存在 `[-2,2]` 的模噪声。
- Next Action: 选择一个模 `q` 下可逆的 `8x8` 子矩阵，结合小噪声枚举或格方法恢复 `s`，再用剩余方程验真。
- Command / Payload / Operation: 用临时 Python 脚本复现 `feature(x)` 并统计 `A` 的形状、样例行和秩。
- Key Result: `A shape=(24, 8)`，首行为 `[59832, 8023, 25545, 21717, 7974, 48814, 25665, 8625]`，矩阵满秩。
- Why It Matters: 这一步证明问题已经被压缩成标准的小维度带噪模线性恢复，可以直接进入求解阶段。

### Step 3
- Category / Skill: `ctf-crypto`
- Fact: 取 8 条线性无关方程后，若枚举这 8 条上的噪声 `e_i ∈ [-2,2]`，则每个噪声向量都会唯一对应一个候选 `s`；再用全部 24 条方程做残差校验即可排除假解。
- Inference: 由于未知维度只有 `8` 且每条噪声只有 `5` 种取值，`5^8 = 390625` 的枚举规模完全可控，比上格工具更直接。
- Next Action: 还原 `s` 的有符号表示，并尝试把它当作 `cipher.bin` 的密钥材料。
- Command / Payload / Operation: 对一组可逆 `8x8` 子矩阵做模逆，枚举 `[-2,2]^8`，并用全部样本筛选候选。
- Key Result: 唯一候选为 `s ≡ [17, 65525, 9, 65522, 6, 14, 65529, 11] (mod 65537)`，中心化后得到 `s = [17, -12, 9, -15, 6, 14, -8, 11]`；24 条方程残差依次为 `[-1, 1, 2, -1, 2, 2, 0, -2, 1, -1, -1, 2, 0, 2, 1, 1, -1, 2, -1, 1, -2, -2, 1, -2]`。
- Why It Matters: 这一步完整证明了秘密头参数已经恢复成功，而且噪声分布完全符合题目给出的界。

### Step 4
- Category / Skill: `ctf-crypto`
- Fact: `cipher.bin` 长度为 `48` 字节，像是 3 个 AES block；`s` 只有 8 个整数，更像先序列化再哈希到 AES 密钥，而不是直接作为原始 16/24/32 字节 key。
- Inference: 先对少量常见序列化方式做最小验证即可，例如 `csv`、`repr(list)`、原始字节，再尝试 `sha256(... )[:16]` 配合 `AES-ECB`。
- Next Action: 固化为 `solve.py`，并整理正式题解 `wp.md`。
- Command / Payload / Operation: 对少量常见 key derivation 和分组模式做最小枚举验证。
- Key Result: 使用 `key = sha256(','.join(map(str, s)).encode()).digest()[:16]`，按 `AES-ECB` 解密得到明文 `flag{7ffd71471b67009e1c39cfaa259cf7b2}`。
- Why It Matters: 题目的最终 flag 已被验证，且整个攻击路径可以脚本化复现。

## Handoff

- Current strongest hypothesis: 已证实这是“公开 CNN 特征抽取 + 小噪声模线性恢复 + 由秘密向量派生 AES 密钥”的组合题。
- Proven: 已恢复 `s = [17, -12, 9, -15, 6, 14, -8, 11]` 并解出 flag `flag{7ffd71471b67009e1c39cfaa259cf7b2}`。
- Next recommended action: 运行 `python solve.py` 做一键复现，并检查 `wp.md` 是否足够清晰。
- Do not repeat: 不需要再走“训练模型”“黑盒拟合网络”之类方向，公开网络在这里仅是生成 LWE 系数的包装器。
