import requests
import json

SOURCE_URL = "https://raw.githubusercontent.com/kenpark76/kenpark76.github.io/main/koreatv.json"
OUTPUT_FILE = "koreatv.json"

LOGO_BASE_URL = "https://faagffxa6sskln.github.io/liveTving/ChannelLogo"

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

remove_titles = ["SBS KPOP", "농협TV", "복지TV", "문화유산채널"]

session = requests.Session()


def main():
    r = session.get(SOURCE_URL, timeout=15)
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
        and item.get("title") not in remove_titles
    ]

    # 2. 중복 제거
    seen_titles = set()
    unique_filtered = []
    for item in filtered:
        title = item.get("title", "")
        if title not in seen_titles:
            unique_filtered.append(item)
            seen_titles.add(title)

    # 3. 로고 적용
    for item in unique_filtered:
        title = item.get("title", "")
        item["logo"] = f"{LOGO_BASE_URL}/{title}.png"

    # 4. 정렬
    priority_items = []
    other_items = []

    for item in unique_filtered:
        if item.get("title") in priority_titles:
            priority_items.append(item)
        else:
            other_items.append(item)

    priority_items.sort(
        key=lambda x: priority_titles.index(x.get("title"))
    )

    final_list = priority_items + other_items

    # 5. 하단 채널
    extra_channels = [
        ("AsiaN", "http://1.214.67.210/vod/65801.m3u8?VOD_RequestID="),
        ("Kstar", "http://1.214.67.210/vod/66201.m3u8?VOD_RequestID="),
        ("GMTV", "http://1.214.67.210/vod/68801.m3u8?VOD_RequestID="),
        ("홈&쇼핑", "http://1.214.67.210/vod/64901.m3u8?VOD_RequestID="),
        ("CJ 온스타일", "http://1.214.67.210/vod/67201.m3u8?VOD_RequestID="),
        ("NS 홈쇼핑", "http://1.214.67.210/vod/67301.m3u8?VOD_RequestID="),
        ("롯데홈쇼핑", "http://1.214.67.210/vod/67401.m3u8?VOD_RequestID="),
        ("현대홈쇼핑", "http://1.214.67.210/vod/67501.m3u8?VOD_RequestID="),
        ("현대홈쇼핑+", "http://1.214.67.210/vod/76001.m3u8?VOD_RequestID="),
        ("GS SHOP", "http://1.214.67.210/vod/67601.m3u8?VOD_RequestID="),
        ("GS MY SHOP", "http://1.214.67.210/vod/74001.m3u8?VOD_RequestID="),
        ("더블유쇼핑", "http://1.214.67.210/vod/81301.m3u8?VOD_RequestID="),
    ]

    existing_titles = {item.get("title") for item in final_list}

    for name, uri in extra_channels:
        if name in existing_titles:
            continue

        final_list.append({
            "group": "한국",
            "name": name,
            "title": name,
            "logo": f"{LOGO_BASE_URL}/{name}.png",
            "uris": [uri]
        })

    # 6. 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} -> {len(final_list)} 완료")


if __name__ == "__main__":
    main()
