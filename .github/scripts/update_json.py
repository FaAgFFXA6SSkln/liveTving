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

    # 1. 필터링
    filtered = [
        item for item in data
        if isinstance(item, dict)
        and "group" in item
        and "한국" in item["group"]
        and item.get("title", "") != "test"
        and "한국영화" not in item.get("title", "")
    ]

    # 2. group 문자열 통일
    for item in filtered:
        item["group"] = "한국"
    
        # 문화유산채널 → 국가유산채널
        if item.get("name") == "문화유산채널" and item.get("title") == "문화유산채널":
            item["name"] = "국가유산채널"
            item["title"] = "국가유산채널"

    # 3. 중복 제거 (title 기준, 뒤쪽 제거)
    seen_titles = set()
    unique_filtered = []
    for item in filtered:
        title = item.get("title", "")
        if title not in seen_titles:
            unique_filtered.append(item)
            seen_titles.add(title)

    # 4. priority / 기타 분리
    priority_items = []
    other_items = []

    for item in unique_filtered:
        if item.get("title") in priority_titles:
            priority_items.append(item)
        else:
            other_items.append(item)

    # priority_titles 순서 유지
    priority_items.sort(
        key=lambda x: priority_titles.index(x.get("title"))
    )

    # 5. SPOTV 항목 삽입
    spotv_item = {
        "group": "한국",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/d/df/SPO_TV_logo.png",
        "name": "SPOTV",
        "title": "SPOTV",
        "uris": [
            "https://211.170.95.22/vod/66701.m3u8?VOD_RequestID=v2M2-0101-1010-7272-5050-000020180717021633"
        ]
    }

    # 혹시 기존 SPOTV가 있으면 제거
    other_items = [
        item for item in other_items
        if item.get("title") != "SPOTV"
    ]

    # 6. 최종 조합
    final_list = priority_items + [spotv_item] + other_items

    # 7. 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} -> {len(final_list)} items (filtered, deduped, reordered)")

if __name__ == "__main__":
    main()
