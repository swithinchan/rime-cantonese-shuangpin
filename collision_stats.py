#!/usr/bin/env python3
"""計算「粵語雙拼（自然碼兼容版）」與粵拼全拼的重碼率。

用法範例：

    python3 collision_stats.py \
        --schema jyutping_nc.schema.yaml \
        --dict /usr/share/rime-data/jyutping.dict.yaml \
        --dict jyutping_nc.dict.yaml

程式會輸出三個統計範圍：
1. 單字詞條
2. 全部詞條
3. 多字詞條（兩個音節或以上）
"""

from __future__ import annotations

import argparse
import collections
import re
from pathlib import Path


RULE_PATTERN = re.compile(
    r"(?P<op>xform|erase|derive|abbrev|fuzz)"
    r"/(?P<pattern>.*?)"
    r"/(?P<replacement>.*?)"
    r"/?\s*(?:#.*)?$"
)


def parse_algebra(schema_text: str) -> list[tuple[str, str, str]]:
    """由 Rime schema 文字抽取 speller.algebra 規則。"""

    rules: list[tuple[str, str, str]] = []
    in_algebra = False
    for raw_line in schema_text.splitlines():
        line = raw_line.strip()
        if line.startswith("algebra:"):
            in_algebra = True
            continue
        if not in_algebra:
            continue
        if not line.startswith("- "):
            continue
        item = line[2:].strip()
        match = RULE_PATTERN.match(item)
        if not match:
            continue
        op = match.group("op")
        pattern = match.group("pattern")
        replacement = match.group("replacement")
        replacement = re.sub(r"\$(\d+)", r"\\g<\1>", replacement)
        rules.append((op, pattern, replacement))
    return rules


def apply_algebra(rules: list[tuple[str, str, str]], code: str) -> str | None:
    """模擬 Rime speller.algebra 對一個全拼碼的索引轉換。"""

    value = code
    for op, pattern, replacement in rules:
        if op in {"xform", "abbrev"}:
            value = re.sub(pattern, replacement, value)
        elif op == "erase":
            if re.search(pattern, value):
                return None
        elif op == "derive":
            # derive 會產生額外輸入碼，不影響主索引碼；此處略過。
            continue
    return value


def parse_dict(path: Path) -> list[tuple[str, str]]:
    """讀取 Rime dictionary，傳回 (字詞, 粵拼碼) 清單。"""

    entries: list[tuple[str, str]] = []
    started = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line
        if line.strip() == "...":
            started = True
            continue
        if not started or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        text = fields[0]
        code = fields[1].strip()
        if code:
            entries.append((text, code))
    return entries


def normalize_syllable(syllable: str) -> str:
    """移除 Jyutping 聲調數字；本雙拼方案忽略聲調。"""

    return re.sub(r"[1-6]+$", "", syllable)


def summarize(rows: list[tuple[str, str, str, int]]) -> dict[str, object]:
    """統計某個範圍內全拼與雙拼的重碼率。"""

    total = len(rows)
    if total == 0:
        return {"total": 0, "full": None, "double": None}

    full_codes = [row[1] for row in rows]
    double_codes = [row[2] for row in rows]
    full_counter = collections.Counter(full_codes)
    double_counter = collections.Counter(double_codes)

    return {
        "total": total,
        "full": {
            "unique": len(full_counter),
            "average": total / len(full_counter),
            "collision_rate": 1.0 - len(full_counter) / total,
            "top": full_counter.most_common(5),
        },
        "double": {
            "unique": len(double_counter),
            "average": total / len(double_counter),
            "collision_rate": 1.0 - len(double_counter) / total,
            "top": double_counter.most_common(5),
        },
    }


def build_rows(
    entries: list[tuple[str, str]],
    rules: list[tuple[str, str, str]],
) -> tuple[list[tuple[str, str, str, int]], int]:
    """將詞條轉成 (字詞, 全拼碼, 雙拼碼, 音節數)，並統計未能編碼的詞條數。"""

    rows: list[tuple[str, str, str, int]] = []
    unsupported = 0
    seen: set[tuple[str, str]] = set()
    for text, code in entries:
        if (text, code) in seen:
            continue
        seen.add((text, code))
        syllables = [normalize_syllable(syllable) for syllable in code.split()]
        mapped = [apply_algebra(rules, syllable) for syllable in syllables]
        if any(value is None for value in mapped):
            unsupported += 1
            continue
        double_code = "".join(value for value in mapped if value is not None)
        full_code = " ".join(syllables)
        rows.append((text, full_code, double_code, len(syllables)))
    return rows, unsupported


def format_table(scope: str, stats: dict[str, object]) -> str:
    lines: list[str] = []
    lines.append(f"### {scope}")
    lines.append("")
    lines.append("| 方案 | 詞條數 | 唯一碼數 | 平均候選／碼 | 重碼率 |")
    lines.append("| --- | ---: | ---: | ---: | ---: |")

    total = int(stats["total"])
    full = stats["full"]
    double = stats["double"]
    if full and double:
        lines.append(
            "| 粵拼全拼 | "
            f"{total:,} | {int(full['unique']):,} | {float(full['average']):.2f} | "
            f"{float(full['collision_rate']) * 100:.2f}% |"
        )
        lines.append(
            "| 本方案雙拼 | "
            f"{total:,} | {int(double['unique']):,} | {float(double['average']):.2f} | "
            f"{float(double['collision_rate']) * 100:.2f}% |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent
    parser.add_argument(
        "--schema",
        type=Path,
        default=default_root / "jyutping_nc.schema.yaml",
        help="Rime schema 路徑（預設：jyutping_nc.schema.yaml）",
    )
    parser.add_argument(
        "--dict",
        type=Path,
        action="append",
        required=True,
        help="Rime dictionary 路徑；可重複傳入，程式會合併去重",
    )
    args = parser.parse_args()

    schema_text = args.schema.read_text(encoding="utf-8")
    rules = parse_algebra(schema_text)

    entries: list[tuple[str, str]] = []
    for dict_path in args.dict:
        if not dict_path.exists():
            parser.error(f"找不到詞庫檔案：{dict_path}")
        entries.extend(parse_dict(dict_path))

    rows, unsupported = build_rows(entries, rules)
    single_rows = [row for row in rows if row[3] == 1]
    multi_rows = [row for row in rows if row[3] >= 2]

    print("# 碰撞率統計")
    print()
    print(f"- 詞條總數（去重後）：{len(rows):,}")
    print(f"- 未能編碼的詞條數：{unsupported:,}")
    print()
    print(format_table("單字", summarize(single_rows)))
    print()
    print(format_table("全部詞條", summarize(rows)))
    print()
    print(format_table("多字詞條", summarize(multi_rows)))
    print()
    print(
        "計算公式：重碼率 = (1 - 唯一碼數 / 詞條數) × 100%；"
        "平均候選／碼 = 詞條數 / 唯一碼數。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
