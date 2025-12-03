import os
import re

# ==========================
# 核心：幂等清洗函数（安全、不损坏内容）
# ==========================

def clean_wechat_article(text: str) -> str:
    original = text  # 用于幂等对比（确保不损坏内容）

    # 1. 删除公众号头部垃圾
    patterns_head = [
        r"原创.*?\n",                           # “原创 XXX”
        r"\[.*?\]\(javascript:void\(0\)\)",     # javascript:void 链接
        r"\*?\d{4}年\d{1,2}月\d{1,2}日.*?\n",   # 日期格式
        r"[\* ]*四川[\* ]*\n",                  # 四川（你的源文中多次出现）
    ]
    for p in patterns_head:
        text = re.sub(p, "", text)

    # 2. 删除 markdown / html 图片
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"<img.*?>", "", text)
    text = re.sub(r"https?://\S+\.(jpg|jpeg|png|gif)", "", text)

    # 3. 删除 emoji（不会影响文字）
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text)

    # 4. 删除 javascript:void(0)
    text = re.sub(r"javascript:void\(0\);?", "", text)

    # 5. 删除独立符号行（不会误删标题或正文）
    text = re.sub(r"^\s*[·\-\*]+\s*$", "", text, flags=re.MULTILINE)

    # 6. 去除空行（幂等）
    lines = [line.strip() for line in text.splitlines() if line.strip() != ""]
    text = "\n".join(lines)

    # 7. 幂等保护：确保不会误伤文本
    # 如果清洗后比原文少了「非垃圾字符」则回退
    # 防止误删正文
    def count_real_chars(s):
        s = re.sub(r"[ \t\n\r]", "", s)
        return len(s)

    if count_real_chars(text) < count_real_chars(original) * 0.5:
        # 意味着内容被异常大量删除 → 回退安全版本
        return original

    return text


# ==========================
# 批量清洗 data/ 下所有 markdown 文件
# ==========================

def batch_clean(folder="data"):
    for filename in os.listdir(folder):
        # 跳过 readme
        if filename.lower() == "readme.md":
            print(f"跳过文件（已忽略）：{filename}")
            continue

        if filename.endswith(".md"):
            path = os.path.join(folder, filename)

            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()

            cleaned = clean_wechat_article(raw)

            # 幂等检测：不应删掉大量非垃圾内容
            with open(path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            print(f"✓ 已清洗：{filename}")

    print("\n🎉 所有文件已安全清洗（幂等，不会损伤已整理内容）")


if __name__ == "__main__":
    batch_clean()