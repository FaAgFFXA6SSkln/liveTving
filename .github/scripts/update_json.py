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

    # 1. '한국'이 포함된 항목만 필터링
    filtered = [
        item for item in data
        if isinstance(item, dict)
        and "group" in item
        and "한국" in item["group"]
    ]

    # 2. group 문자열 공백 처리
    for item in filtered:
        item["group"] = ""

    # 3. priority_titles에 있는 항목을 맨 위로 정렬
    def sort_key(item):
        # 우선순위 목록에 있으면 인덱스로, 없으면 큰 숫자
        try:
            return priority_titles.index(item.get("title", "")), 0
        except ValueError:
            return len(priority_titles), 0

    filtered.sort(key=sort_key)

    # 4. 파일로 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} -> {len(filtered)} items")

if __name__ == "__main__":
    main()
