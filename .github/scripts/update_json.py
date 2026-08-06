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


# ✅ 공용 세션 (Agent 역할)
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://onair.kbs.co.kr/",
    "Accept": "application/json, text/plain, */*"
})


# ✅ KBS 스트림 가져오기
def get_kbs_stream(ch_code):
    try:
        url = f"https://cfpwwwapi.kbs.co.kr/api/v1/landing/live/channel_code/{ch_code}"

        r = session.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()
        stream = data["channel_item"][0]["service_url"]

        print(f"[KBS {ch_code}] 성공:", stream)
        return stream

    except Exception as e:
        print(f"[KBS {ch_code}] 실패:", e)
        return None


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


"""
    # 2. 수정
    for item in filtered:
        item["group"] = "한국"

        if item.get("name") == "SBS":
            item["uris"] = ["http://1.222.207.80:1935/live/cjbtv/chunklist_w1909627462.m3u8"]

        if item.get("name") == "MBC":
            item["uris"] = ["https://stream.chmbc.co.kr/TV/myStream/chunklist_w641999880.m3u8"]

        if item.get("name") == "YTN":
            item["uris"] = ["https://1.214.67.206/vod/69801.m3u8?VOD_RequestID="]

        if item.get("name") == "TV CHOSUN":
            item["uris"] = ["https://1.214.67.206/vod/74601.m3u8?VOD_RequestID="]

        # ✅ KBS 동적 처리

        if item.get("name") == "KBS2":
            url = get_kbs_stream(12)
            if url:
                item["uris"] = [url]
            else:
                #item["uris"] = ["FAILED_KBS2"]
                item["uris"] = ["http://1.214.67.210/vod/50201.m3u8?VOD_RequestID="]
                
"""

    # 3. 중복 제거
    seen_titles = set()
    unique_filtered = []
    for item in filtered:
        title = item.get("title", "")
        if title not in seen_titles:
            unique_filtered.append(item)
            seen_titles.add(title)

    # 4. 로고 적용
    for item in unique_filtered:
        title = item.get("title", "")
        item["logo"] = f"{LOGO_BASE_URL}/{title}.png"

    # 5. 정렬
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

    # 6. 하단 채널
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

    # 7. 저장
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"{len(data)} -> {len(final_list)} 완료")


if __name__ == "__main__":
    main()
