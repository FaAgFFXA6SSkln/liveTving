import requests
import json

SOURCE_URL = "https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatv.json"
OUTPUT_FILE = "koreatv.json"

# 우선순위로 맨 위로 올릴 title 목록
priority_titles = [
    "SBS",
    "KBS2",
    "KBS1",
    "MBC",
    "EBS1",
    "JTBC",
    "TV CHOSUN",
    "MBN",
    "채널A",
    "tvN",
    "Mnet"
]

def main():
    r = requests.get(SOURCE_URL, timeout=15)
    r.raise_for_status()

    data = r.json()

    if not isinstance(data, list):
        raise RuntimeError("JSON root is not a list")

    # 1. '한국'이 포함된 항목만 필터링 + title != "test"
    filtered = [
        item for item in data
        if isinstance(item, dict)
        and "group" in item
        and "한국" in item["group"]
        and item.get("title", "") != "test"
        and "한국영화" not in item.get("title", "")
    ]

    # 2. group 문자열 "한국"으로 통일
    for item in filtered:
        item["group"] = "한국"

    # 3. 중복 제거 (title 기준, 뒤쪽 제거)
    seen_titles = set()
    unique_filtered = []
    for item in filtered:
        title = item.get("title", "")
        if title not in seen_titles:
            unique_filtered.append(item)
            seen_titles.add(title)
        # 중복이면 스킵 (뒤쪽 제거)

    # 4. priority_titles에 있는 항목을 맨 위로 정렬
    def sort_key(item):
        try:
            return priority_titles.index(item.get("title", "")), 0
        except ValueError:
            return len(priority_titles), 0

    unique_filtered.sort(key=sort_key)

    # 5. 파일로 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique_filtered, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} -> {len(unique_filtered)} items (duplicates removed, 'test' excluded)")

if __name__ == "__main__":
    main()
