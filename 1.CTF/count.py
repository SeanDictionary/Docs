from pathlib import Path
import time

BLACKLIST = ["0.工具列表", "AWD-祖传妙妙文档", "qsnctf"]
TYPE = ['.md', '.txt']

def main():
    script_dir = Path(__file__).resolve().parent
    f = open(script_dir / "count.log", "a", encoding="utf-8")

    def print(a):
        f.write(str(a) + '\n')
        __builtins__['print'](a)

    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    root = script_dir

    total = 0
    size = 0
    files = list(root.rglob('*'))
    for p in files:
        if not p.is_file():
            continue
        # 检查是否在黑名单目录下
        rel_parts = p.relative_to(root).parts
        if any(part in BLACKLIST for part in rel_parts):
            continue
        if p.suffix.lower() in TYPE:
            text = p.read_text(encoding='utf-8', errors='ignore')
            count = len(text)
            print(f"{count:6d} | {p.relative_to(root)}")
            total += count

            size += p.stat().st_size

    print("-" * 40)
    print(f"Total characters: {total}")
    print(f"Total size: {size} bytes\n")


if __name__ == '__main__':
    main()
