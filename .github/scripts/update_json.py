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

remove_titles = [
    "SBS KPOP",
    "농협TV",
    "복지TV",
    "문화유산채널"
]

session = requests.Session()


def main():
    # 1. 외부 JSON 가져오기
    r = session.get(SOURCE_URL, timeout=15)
    r.raise_for_status()

    data = r.json()

    if not isinstance(data, list):
        raise RuntimeError("JSON root is not a list")

    # 2. 필터링
    filtered = [
        item
        for item in data
        if isinstance(item, dict)
        and "group" in item
        and "한국" in item["group"]
        and item.get("title", "") != "test"
        and "한국영화" not in item.get("title", "")
        and item.get("title") not in remove_titles
    ]

    # 3. 중복 제거
    seen_titles = set()
    unique_filtered = []

    for item in filtered:
        title = item.get("title", "")

        if title not in seen_titles:
            unique_filtered.append(item)
            seen_titles.add(title)

    # 4. group 및 로고 적용
    for item in unique_filtered:
        title = item.get("title", "")

        # 모든 외부 채널의 group을 한국으로 통일
        item["group"] = "한국"

        # 로고 적용
        item["logo"] = f"{LOGO_BASE_URL}/{title}.png"

    # 5. 우선순위 정렬
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

    # 6. 하단 추가 채널
    extra_channels = [
        ("홈&쇼핑", "https://s34.qtcdn.co.kr/media/liveM3U8/idx/710401216/enc/1728755331/playlist.m3u8"),
        ("CJ 온스타일", "https://live-ch1.cjonstyle.net/cjmalllive/stream2/playlist.m3u8"),
        ("NS 홈쇼핑", "https://shoppstream.nsmall.com/IPHONE/mobile.m3u8"),
        ("롯데홈쇼핑", "https://onetvhlslive.lotteimall.com/lotteonetvlive/lotteonetvlive.mp4.m3u8"),
        ("현대홈쇼핑", "https://livejj.hyundaihmall.com:8443/live/ngrp:hmall.stream_pc/playlist.m3u8"),
        ("현대홈쇼핑+", "https://dtvstreaming.hyundaihmall.com/newcjp3/_definst_/newcjpstream.smil/playlist.m3u8"),
        ("GS SHOP", "https://gstv-gsshop.gsshop.com/gsshop_hd/_definst_/gsshop_hd.stream/playlist.m3u8"),
        ("GS MY SHOP", "https://gstv-myshop.gsshop.com/myshop_hd/myshop_hd.stream/playlist.m3u8"),
        ("더블유쇼핑", "https://liveout.catenoid.net/live-05-wshopping/wshopping_1500k/playlist.m3u8"),
        ("신세계 쇼핑", "https://liveout.catenoid.net/live-02-shinsegaetvshopping/shinsegaetvshopping_720p/playlist.m3u8"),
        ("쇼핑엔티", "https://live.shoppingntmall.com/live/10011.m3u8")
    ]

    existing_titles = {
        item.get("title")
        for item in final_list
    }

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
        json.dump(
            final_list,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"{len(data)} -> {len(final_list)} 완료")


if __name__ == "__main__":
    main()
